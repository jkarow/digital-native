# Digital Native

An experimental set of primaries aiming for the ideal oxymoron of a camera-agnostic camera native space.

![](https://user-images.githubusercontent.com/66244111/277839781-3b2a9a0d-723e-42ad-b3fb-b6d64663b5c5.png)

Each primary is chosen either directly from or fitted to a dataset of virtual primaries extrapolated from known camera matrices. This is very much brute-force.

The source files are of the form:

```
dignat-DATASET-FIT_METHOD.py
```

## Matrices

Old don't use.

DigNat to XYZ D65:

```
0.95862252 -0.05840237  0.05023578
0.38338622  0.89185891 -0.27524513
0.04954812 -0.46386142  1.50337105
```

XYZ D65 to DigNat:

```
 1.02266986 0.05437236 -0.02421817
-0.49738313 1.21281632  0.2386691 
-0.1871715  0.37241947  0.73961072
```
