# GAN-indiv-study
It's a part of my indiv course about GAN 

# Table of Contents
- [Introduction](#introduction)
- [Dataset](#dataset)
    1. [AJDATASET01](#ajdataset01)
    1. [AJDATASET02](#ajdataset02)
    1. [AJDATASET03M](#ajdataset03m)
- [Environment](#environment)
- [Experiment](#experiment)
    1. [pure_data_same_model_as_BDD](#pure_data_same_model_as_bdd)
    1. [augmented_ajdataset](#augmented_ajdataset)
    1. [same_load_and_fine_size_better_resol](#same_load_and_fine_size_better_resol)
    1. [medium_size_dataset_basic](#medium_size_dataset_basic)
    1. [small_size_dataset_fine_tune_BDD100K](#small_size_dataset_fine_tune_bdd100k)
- [Conclusion from above experiment](#conclusion-from-above-experiments)
- [Final model and result](#final-model-and-result)
- [Utilization in this repo](#utilization-in-this-repo)
    1. [Image extraction from video](#image-extraction-from-video)
- [Resources](#resources)


# Introduction
TODO
# Dataset
## AJDATASET01
- Only from 1 video (**2021_0607_184742_013.MOV**) 
    - extract every 10 second.
- Total `264 images`
    - Train : `236 images`
        - Day : `67 images`
        - Night : `169 images`
    - Test : `28 images`
        - Day : `7 images`
        - Night : `21 images`

## AJDATASET02
- Original video
    1. `2021_0607_184742_013.MOV`
    1. `Top.MOV`
    - extract every 10 second
    > different location
- Total `390 images`
    - Train : `300 images`
        - Day : `150 images`
        - Night : `150 images`
    - Test : `90 images`
        - Day : `50 images`
        - Night : `40 images`

## AJDATASET03M
> **M** is stand for medium.
- Original video
    1. `2021_0610_194042_002.MOV` (Night video)
    1. `2021_0610_135731_008.MOV` (Day video)
    - extract every 2 second.
    > same location, different time
- Total `4,090 images` 
    - Train : `3,700 images`
        - Day : `1,853 images`
        - Night : `1,847 images`
    - Test : `390 images`
        - Day : `190 images`
        - Night : `200 images`

# Environment
This repo use the same environment as [**GAN-study**](#resources) repo.

TODO - breifly explain
# Experiment
> **FYI** : This part is my logs of my exploration feel free to skip this and read [Conclusion part](#conclusion-from-above-experiments)
## pure_data_same_model_as_BDD
> Use the same model structure that used in BDD100k dataset to train `AJDATASET01`
### Setting
```bash
python main.py --dataset_dir AJDATASET01 \  
                --phase train \
                --experiment_name pure_data_same_model_as_BDD \
                --batch_size 2  \
                --load_size 286 \
                --fine_size 128 \
                --epoch 30 \
                --use_uncertainty True
```
- Batch size : `2`
- Load size : `286`
- Fine size : `128`
- Epoch : `30`
- Use uncertainty : `True`
- Learning rate : `0.0002`
- Dataset : [`AJDATASET01`](#ajdataset01)
### Result
- example for *Night to Day*

    ![AtoB](./asset/pure_data_same_model_as_BDD/AtoB.jpg)
- example for *Day to Night*

    ![BtoA](./asset/pure_data_same_model_as_BDD/BtoA.jpg)
### Analysis
1. Night and Day image in dataset are too similar.
    - e.g. In the both day and night image, every car has the light on 
    - This make the translated image very similar to the original image.
1. The resolution of model is very low (256x128) so might not able to count the car.

## augmented_ajdataset
> Use `AJDATASET02` which create from 2 videos in different time and location to train.
### Setting
```bash
python main.py --dataset_dir AJDATASET02 \
                --phase train \
                --experiment_name augmented_ajdataset \
                --batch_size 2  \
                --load_size 286 \
                --fine_size 128 \
                --epoch 30 \
                --use_uncertainty True \
```
- Batch size : `2`
- Load size : `286`
- Fine size : `128`
- Epoch : `30`
- Use uncertainty : `True`
- Learning rate : `0.0002`
- Dataset : [`AJDATASET02`](#ajdataset02)
### Result
- example for *Night to Day*

    ![AtoB](./asset/augmented_ajdataset/AtoB.jpg)
- example for *Day to Night*

    ![BtoA](./asset/augmented_ajdataset/BtoA.jpg)
### Analysis
1. Can't use translated image to do anything.
    - The previous infomation such as car, road, etc. are gone.
    - This may cause by **load size** and **fine size** are too different.
1. Maybe **learning rate** are not relate with **new batch-size**
    - According to [Krizhevsky. One weird trick for parallelizing convolutional neural networks](https://arxiv.org/abs/1404.5997), if we multiply the batch size by k, we multiply the learning rate by square root of k as well.

## same_load_and_fine_size_better_resol
> Try to create translation on (512x256) resolution image.
### Setting
```bash
python main.py --dataset_dir AJDATASET01 \
                --phase train \
                --experiment_name same_load_and_fine_size_better_resol \
                --batch_size 1 \
                --load_size 286 \
                --fine_size 256 \
                --epoch 20 \
                --use_uncertainty True \
```
- Batch size : `1`
- Load size : `286`
- Fine size : `256`
- Epoch : `20`
- Use uncertainty : `True`
- Learning rate : `0.0002`
- Dataset : [`AJDATASET01`](#ajdataset01)
### Result
- example for *Night to Day*

    ![AtoB](./asset/same_load_and_fine_size_better_resol/AtoB.jpg)
- example for *Day to Night*

    ![BtoA](./asset/same_load_and_fine_size_better_resol/BtoA.jpg)
### Analysis
1. The resolution is better than before.
    - Compare to [pure_data_same_model_as_BDD](#pure_data_same_model_as_bdd) experiment.
1. With better resolution and the more close between **load size** and **fine size**.
    - The translation is better than before.

## medium_size_dataset_basic
> Another point of view([AJDATASET03M](#ajdataset03m)) to train the model.
> The benefits is the dataset is bigger than before.
### Setting
```bash
python main.py --dataset_dir AJDATASET03M \
                --phase train \
                --experiment_name medium_size_dataset_basic \
                --batch_size 1 \
                --load_size 286 \
                --fine_size 256 \
                --epoch 5 \
                --use_uncertainty True \
                --lr 0.00007
```
- Batch size : `1`
- Load size : `286`
- Fine size : `256`
- Epoch : `5`
- Use uncertainty : `True`
- Learning rate : `0.00007`
- Dataset : [`AJDATASET03M`](#ajdataset03m)
### Result
- example for *Night to Day*

    ![AtoB](./asset/medium_size_dataset_basic/AtoB.jpg)
- example for *Day to Night*

    ![BtoA](./asset/medium_size_dataset_basic/BtoA.jpg)

### Analysis

## small_size_dataset_fine_tune_BDD100K
> Try to fix about small dataset problem by fine tune the model that trained by BDD100K dataset.
### Setting
### Result
- example for *Night to Day*

    ![AtoB](./asset/small_size_dataset_fine_tune_BDD100K/AtoB.jpg)

- example for *Day to Night*

    ![BtoA](./asset/small_size_dataset_fine_tune_BDD100K/BtoA.jpg)

### Analysis

# Conclusion from above experiments
## Load size and fine size in train phase
$$\text{Load size} - \text{Fine size}  \text{ be small value e.g. 30 and non-negative }$$
According to the original implementation in the train process, The model will load image as (`Load size x 2`, `Load size`) pixel then crop image size (`Fine size x 2`, `Fine size`) and **random position** to be train image.
Thus, if Load size and Fine size is very different the model might not learn from the correct image pair.
## Learning rate and Batch size relationship
From [Krizhevsky. One weird trick for parallelizing convolutional neural networks](https://arxiv.org/abs/1404.5997), If we multiply batch size with $K$, we must multiply learning rate with $\sqrt{K}$ to keep the variance in the gradient expectation constant.
# Final model and result
> The trained weight is on [Google drive]()
TODO

# Utilization in this repo
## Image extraction from video
This use to extract images from video and save it to the folder. 
It's able to extract infomation from image
1. If video's name is fit the `yyyy_mmdd_hhmmss_ffff` format, `info_dict` will save the time information of each image.
1. The image labels to **night** if the time is between 18:00 to 6:00, and **day** if the time is between 6:00 to 18:00. **except**
    - `Top.MOV` is **day** image


The code is in [Indiv_image](./Indiv_image/) which has 2 files.
1. [image_extractor.py](./Indiv_image/image_extractor.py) is used to extract 
images from video. as python script

    Usage 
    ```bash 
    python ./indiv_image/image_extractor.py --clip_path <path to video> \    
                                            --image_path <path to save image> \
                                            --info_path <path to save info>
    ```
<!-- 
python image_extractor.py --clip_path E:/indiv_vdo/2021_0610_194042_002.MOV --image_path E:/indiv_vdo/extracted/image_pool --info_path E:/indiv_vdo/extracted/info_pool
 -->

1. [image_extractor.ipynb](./Indiv_image/image_extractor.ipynb) is used to extract images from video. as jupyter notebook

## Resources

1. AU-GAN
    - Official implementation : [Github](https://github.com/jgkwak95/AU-GAN)
    - Paper : [pdf here](https://www.bmvc2021-virtualconference.com/assets/papers/1443.pdf)
1. DCGANs -- [pdf here](https://arxiv.org/pdf/1511.06434.pdf)
1. WGANs -- [pdf here](https://arxiv.org/pdf/1701.07875.pdf)
1. Improved Training of Wasserstein GANs -- [pdf here](https://arxiv.org/pdf/1704.00028.pdf)
1. Krizhevsky. One weird trick for parallelizing convolutional neural networks -- [pdf here](https://arxiv.org/abs/1404.5997)