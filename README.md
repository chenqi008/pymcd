## Project description

This package (pymcd) computes Mel Cepstral Distortion (MCD) in python, which is used to assess the quality of the generated speech by comparing the discrepancy between generated and ground-truth speeches.

## Overview

Mel Cepstral Distortion (MCD) is a measure of how different two sequences of mel cepstra are, which is widely used to evaluate the performance of speech synthesis models. The MCD metric compares k-th (default k=13) Mel Frequency Cepstral Coefficient (MFCC) vectors derived from the generated speech and ground truth, respectively.

The pymcd package provides scripts to compute a variety of forms of MCD score:

- MCD (plain): the conventional MCD metric, which requires the lengths of two input speeches to be the same. Otherwise, it would simply extend the shorted speech to the length of longer one by padding zero for the time-domain waveform.
- MCD-DTW: an improved MCD metric that adopts the Dynamic Time Warping (DTW) algorithm to find the minimum MCD between two speeches.
- MCD-DTW-SL: MCD-DTW weighted by Speech Length (SL) evaluates both the length and the quality of alignment between two speeches. Based on the MCD-DTW metric, the MCD-DTW-SL incorporates an additional coefficient w.r.t. the difference between the lengths of two speeches. 

More details of the above three types of MCD can be found in [V2C: Visual Voice Cloning](https://openaccess.thecvf.com/content/CVPR2022/papers/Chen_V2C_Visual_Voice_Cloning_CVPR_2022_paper.pdf).

## License

Please see the file License for details of the license and warranty for mcd.

## Installation

Require Python 3, the package can be installed and updated using pip, i.e.,

```
pip install -U pymcd
```

## Example

```
from pymcd.mcd import Calculate_MCD

# instance of MCD class
# three different modes "plain", "dtw" and "dtw_sl" for the above three MCD metrics
mcd_toolbox = Calculate_MCD(MCD_mode="plain")

# two inputs w.r.t. reference (ground-truth) and synthesized speeches, respectively
mcd_value = mcd_toolbox.calculate_mcd("001.wav", "002.wav")

```



