# Digital Native

An experimental set of primaries aiming for the ideal oxymoron of a camera-agnostic camera native space.

Each primary is chosen from a dataset consisting of extrapolated virtual primaries from cameras with known matrices.

![](https://user-images.githubusercontent.com/66244111/277140183-9dae451c-0de9-46c7-b88e-b6be8da7a542.png)
![](https://user-images.githubusercontent.com/66244111/277622033-df7af8aa-5a00-4c1f-891a-b76d8092d12d.png)

This is very much brute-force. There's no rotational scaling or correction, and it relies on general similarity.

## Matrices

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
