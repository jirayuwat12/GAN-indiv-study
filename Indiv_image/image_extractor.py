import os
import cv2    
import argparse
import pickle
import tqdm
import numpy as np

def fetch_and_show_images(clip_path,
                          save_dir,
                          capture_interval=20,
                          replace=False,
                          verbose=True,
                          resolution=(512, 256)
                          ):
    """
    Fetch images from a clip, save as individual files, then visualize using subplots.
    
    Parameters:
    - clip_path (str): Path to the video clip.
    - save_dir (str): Folder to save the fetched images.
    - capture_interval (int): Span to fetch images. Default is 20 seconds.
    - replace (bool): If True, replace existing images with the same name. Default is False.
    - verbose (bool): If True, print out the process. Default is True.
    """

    clip_name = clip_path.split('/')[-1].split('.')[0]

    # Verify if save directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # Initialize video reader
    clip_reader = cv2.VideoCapture(clip_path)
    frame_total = int(clip_reader.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(clip_reader.get(cv2.CAP_PROP_FPS))
    duration = frame_total // fps

    if verbose:
        print(f"Extracting {clip_name}")
        print(f"Frames available in the clip: {frame_total} ({duration} sec.)")
        print(f"Fetching every {capture_interval} second or {fps * capture_interval} frames")
    capture_interval *= fps

    current_frame = 0
    fetched_count = 0

    while True:
        # Read frame
        status, image = clip_reader.read()

        # If reading frame fails, exit the loop
        if not status:
            break

        if current_frame % capture_interval == 0:
            # resize image
            image = cv2.resize(image, resolution)

            image_filename = f"{clip_name}-{int(current_frame/fps)}.png"
            image_filepath = save_dir + '/' + image_filename

            if not os.path.exists(image_filepath) or replace:
                cv2.imwrite(image_filepath, image)
                if verbose:
                    print(f"Fetched frame {current_frame}({100*current_frame/frame_total:.2f}%) as {image_filename}")
            elif verbose:
                print(f"Image {image_filename} already exists, skipping...")
            fetched_count += 1

        current_frame += 1

    clip_reader.release()

    if verbose:
        print(f"Process complete! Fetched {fetched_count} frames from the clip.")

def get_datetime(img):
    '''
    Get datetime from image name
    on assumtion that file name is on format: 'yyyy_mmdd_hhmmss_fff-t.png'
    which
        yyyy_mmdd_hhmmss_fff is started record datetime
        t is time from started record datetime (sec.)
    '''
    try:
        # remove file extension
        img = img.split('.')[0]

        # get datetime from file name
        start_record_datetime = img.split('-')[0]
        start_record_datetime = dt.datetime.strptime(start_record_datetime, '%Y_%m%d_%H%M%S_%f')

        # get time from started record datetime
        time_from_start_record = img.split('-')[1]
        time_from_start_record = dt.timedelta(seconds=int(time_from_start_record))

        # get datetime from image
        img_datetime = start_record_datetime + time_from_start_record

        return img_datetime
    except:
        return None


parser = argparse.ArgumentParser(description='Extract image and info from video')
# data path
parser.add_argument('--clip_path',
                    dest='clip_path',
                    type=str,
                    default=None,
                    help='path to the video clip',
                    required=True)
parser.add_argument('--image_path',
                    dest='image_path',
                    type=str,
                    default='./image_pool',
                    help='path for the image folder')
parser.add_argument('--info_path',
                    dest='info_path',
                    type=str,
                    default='./info_pool',
                    help='path for the info folder')

# extract image
parser.add_argument('--extract_image',
                    dest='extract_image',
                    type=bool,
                    default=True,
                    help='extract image from the video clip')
parser.add_argument('--replace',
                    dest='replace',
                    type=bool,
                    default=False,
                    help='replace existing images with the same name')
parser.add_argument('--resolution',
                    type=tuple,
                    default=(512, 256),
                    help='resolution of the extracted images')
parser.add_argument('--verbose',
                    type=bool,
                    default=True,
                    help='print out the process')
parser.add_argument('--capture_interval',
                    type=int,
                    default=10,
                    help='span to fetch images. Default is 10 seconds.')

# extract info
parser.add_argument('--extract_info',
                    type=bool,
                    default=True,
                    help='extract info from the video clip')

# show summary
parser.add_argument('--show_summary',
                    dest='show_summary',
                    type=bool,
                    default=True,
                    help='show summary of the extracted info')

args = parser.parse_args()


if __name__ == '__main__':
    # extract image from the video clip
    if args.extract_image:
        fetch_and_show_images(args.clip_path,
                              args.image_path,
                              args.capture_interval,
                              args.replace,
                              args.verbose,
                              args.resolution
                              )

    # extract info from the extracted images
    clip_name = args.clip_path.split('/')[-1].split('.')[0]
    info_dict = {}
    if args.extract_info:
        if not os.path.exists(args.info_path):
            os.makedirs(args.info_path)

        if not os.path.exists(args.info_path + '/' + clip_name + '_info.pkl'):
            with open(args.info_path + '/' + clip_name + '_info.pkl', 'wb') as f:
                pickle.dump({}, f)

        with open(args.info_path + '/' + clip_name + '_info.pkl', 'rb') as f:
            info_dict = pickle.load(f)

    image_name_list = os.listdir(args.image_path)
    looper = tqdm.tqdm(image_name_list, unit='image')
    for image_name in looper:
        looper.set_description(f'Processing {image_name}')

        if image_name not in info_dict:
            info_dict[image_name] = dict()

        ## get datetime from image
        img_datetime = get_datetime(image_name)

        info_dict[image_name]['datetime'] = img_datetime

        ## get image shape
        image = cv2.imread(args.image_path + '/' + image_name)
        info_dict[image_name]['shape'] = image.shape

        ## get avg intensity
        gray_image = cv2.imread(args.image_path + '/' + image_name, cv2.IMREAD_GRAYSCALE)
        avg_intensity = np.mean(gray_image)

        info_dict[image_name]['avg_intensity'] = avg_intensity

        ## get original vdo name
        info_dict[image_name]['vdo_name'] = image_name.split('-')[0] + '.MOV'

        ## label it's day or night(7pm - 6am)
        if img_datetime is None:
            # if vdo name is Top.MOV, then it's day
            if info_dict[image_name]['vdo_name'] == 'Top.MOV':
                info_dict[image_name]['day_night'] = 'day'
        elif img_datetime.hour >= 19 or img_datetime.hour <= 6:
            info_dict[image_name]['day_night'] = 'night'
        else:
            info_dict[image_name]['day_night'] = 'day'

    # save info
    with open(args.info_path + '/' + clip_name + '_info.pkl', 'wb') as f:
        pickle.dump(info_dict, f)

    # show summary
    if args.show_summary:
        # read info dict
        night_image_name_list = []
        day_image_name_list = []
        other_image_name_list = []
        total_image_amount = len(info_dict)
        original_vdo_count = dict()

        for image_name in tqdm.tqdm(info_dict):
            # add image name to list
            if 'day_night' not in info_dict[image_name]:
                other_image_name_list.append(image_name)
            elif info_dict[image_name]['day_night'] == 'night':
                night_image_name_list.append(image_name)
            elif info_dict[image_name]['day_night'] == 'day':
                day_image_name_list.append(image_name)
            else:
                other_image_name_list.append(image_name)

            # add original vdo name to dict
            if info_dict[image_name]['vdo_name'] not in original_vdo_count:
                original_vdo_count[info_dict[image_name]['vdo_name']] = 1
            else:
                original_vdo_count[info_dict[image_name]['vdo_name']] += 1

        print(f'[x] Total amount of image: {total_image_amount}')
        print(f'[x] Amount of day image: {len(day_image_name_list)}({len(day_image_name_list)/total_image_amount*100:.2f}%)')
        print(f'[x] Amount of night image: {len(night_image_name_list)}({len(night_image_name_list)/total_image_amount*100:.2f}%)')

        print('[x] Count of image from each original vdo')
        for vdo_name in original_vdo_count:
            print(f'\t- {vdo_name}: {original_vdo_count[vdo_name]}')
