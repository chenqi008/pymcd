import librosa
import math
import numpy as np
import pyworld
import pysptk
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean


# ================================================= #
# calculate the Mel-Cepstral Distortion (MCD) value #
# ================================================= #
class Calculate_MCD(object):
	"""docstring for Calculate_MCD"""
	def __init__(self, MCD_mode):
		super(Calculate_MCD, self).__init__()
		# self.args = args
		self.MCD_mode = MCD_mode
		self.SAMPLING_RATE = 22050
		self.FRAME_PERIOD = 5.0
		self.log_spec_dB_const = 10.0 / math.log(10.0) * math.sqrt(2.0) # 6.141851463713754
	
	def load_wav(self, wav_file, sample_rate):
		"""
		Load a wav file with librosa.
		:param wav_file: path to wav file
		:param sr: sampling rate
		:return: audio time series numpy array
		"""
		wav, _ = librosa.load(wav_file, sr=sample_rate, mono=True)
		return wav

	# distance metric
	def log_spec_dB_dist(self, x, y):
		# log_spec_dB_const = 10.0 / math.log(10.0) * math.sqrt(2.0)
		diff = x - y
		return self.log_spec_dB_const * math.sqrt(np.inner(diff, diff))

	# calculate distance (metric)
	# def calculate_mcd_distance(self, x, y, distance, path):
	def calculate_mcd_distance(self, x, y, path):
		'''
		param path: pairs between x and y
		'''
		pathx = list(map(lambda l: l[0], path))
		pathy = list(map(lambda l: l[1], path))
		x, y = x[pathx], y[pathy]
		frames_tot = x.shape[0]       # length of pairs

		z = x - y
		min_cost_tot = np.sqrt((z * z).sum(-1)).sum()

		return frames_tot, min_cost_tot

	# extract acoustic features
	# alpha = 0.65  # commonly used at 22050 Hz
	def wav2mcep_numpy(self, loaded_wav, alpha=0.65, fft_size=512):

		# Use WORLD vocoder to spectral envelope
		_, sp, _ = pyworld.wav2world(loaded_wav.astype(np.double), fs=self.SAMPLING_RATE,
									   frame_period=self.FRAME_PERIOD, fft_size=fft_size)

		# Extract MCEP features
		mcep = pysptk.sptk.mcep(sp, order=13, alpha=alpha, maxiter=0,
							   etype=1, eps=1.0E-8, min_det=0.0, itype=3)

		return mcep

	# calculate the Mel-Cepstral Distortion (MCD) value
	def average_mcd(self, ref_audio_file, syn_audio_file, cost_function, MCD_mode):
		"""
		Calculate the average MCD.
		:param ref_mcep_files: list of strings, paths to MCEP target reference files
		:param synth_mcep_files: list of strings, paths to MCEP converted synthesised files
		:param cost_function: distance metric used
		:param plain: if plain=True, use Dynamic Time Warping (dtw)
		:returns: average MCD, total frames processed
		"""
		# load wav from given wav file
		loaded_ref_wav = self.load_wav(ref_audio_file, sample_rate=self.SAMPLING_RATE)
		loaded_syn_wav = self.load_wav(syn_audio_file, sample_rate=self.SAMPLING_RATE)

		if MCD_mode == "plain":
			# pad 0
			if len(loaded_ref_wav)<len(loaded_syn_wav):
				loaded_ref_wav = np.pad(loaded_ref_wav, (0, len(loaded_syn_wav)-len(loaded_ref_wav)))
			else:
				loaded_syn_wav = np.pad(loaded_syn_wav, (0, len(loaded_ref_wav)-len(loaded_syn_wav)))

		# extract MCEP features (vectors): 2D matrix (num x mcep_size)
		ref_mcep_vec = self.wav2mcep_numpy(loaded_ref_wav)
		syn_mcep_vec = self.wav2mcep_numpy(loaded_syn_wav)

		if MCD_mode == "plain":
			# print("Calculate plain MCD ...")
			path = []
			# for i in range(num_temp):
			for i in range(len(ref_mcep_vec)):
				path.append((i, i))
		elif MCD_mode == "dtw":
			# print("Calculate MCD-dtw ...")
			_, path = fastdtw(ref_mcep_vec[:, 1:], syn_mcep_vec[:, 1:], dist=euclidean)
		elif MCD_mode == "dtw_sl":
			# print("Calculate MCD-dtw-sl ...")
			cof = len(ref_mcep_vec)/len(syn_mcep_vec) if len(ref_mcep_vec)>len(syn_mcep_vec) else len(syn_mcep_vec)/len(ref_mcep_vec)
			_, path = fastdtw(ref_mcep_vec[:, 1:], syn_mcep_vec[:, 1:], dist=euclidean)

		frames_tot, min_cost_tot = self.calculate_mcd_distance(ref_mcep_vec, syn_mcep_vec, path)

		if MCD_mode == "dtw_sl":
			mean_mcd = cof * self.log_spec_dB_const * min_cost_tot / frames_tot
		else:
			mean_mcd = self.log_spec_dB_const * min_cost_tot / frames_tot

		return mean_mcd

	# calculate mcd
	def calculate_mcd(self, reference_audio, synthesized_audio):
		# extract acoustic features
		mean_mcd = self.average_mcd(reference_audio, synthesized_audio, self.log_spec_dB_dist, self.MCD_mode)

		return mean_mcd
