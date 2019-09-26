import argparse
import joblib
import os
import cv2

def parse_args():
    parser = argparse.ArgumentParser(
        description='visulize the image sequeces with ground truth bouding boxes and arm signals')
    parser.add_argument('--dataset', required=True,
                        help='youtube or casr')
    parser.add_argument('--track_number', required=True,
                        help='youtube track number from 0 to 8. '
                             'casr track number from 0 to 178.')
    args = parser.parse_args()

    return args


def main(dataset, track_number):
    annotation = joblib.load(os.path.join('data', 'annotations', dataset+'_annotation.pickle'))[int(track_number)]
    video_folder = annotation[0]['video_folder']
    vis_folder = os.path.join('data', 'visualization')
    if not os.path.exists(vis_folder):
        os.mkdir(vis_folder)
    save_track = os.path.join('data', 'visualization', dataset+'_track_'+track_number)
    if not os.path.exists(save_track):
        os.mkdir(save_track)
    for i,frame in enumerate(annotation):
        img_fname = annotation[i]['frame_idx']
        img = cv2.imread(os.path.join('data', 'images', video_folder, img_fname))
        bbox = annotation[i]['bbox_gt']
        x1, y1, bb_w, bb_h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        x2 = bb_w + x1
        y2 = bb_h + y1
        bb_color = (0, 0, 255)
        cv2.rectangle(img, (x1,y1), (x2,y2),bb_color,3)
        action_label_gt = annotation[i]['left_or_right']
        if action_label_gt==0:
            gt_text = 'Left'
        elif action_label_gt==1:
            gt_text = 'Right'
        elif action_label_gt==2:
            gt_text = 'Stop'
        elif action_label_gt==3:
            gt_text = 'No Signal'
        else:
            gt_text = 'Something Wrong'
        cv2.putText(img, 'GT:  '+gt_text, (x1 + 20, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0, 255, 0), 3)
        cv2.imwrite(os.path.join(save_track, img_fname), img)



if __name__ == '__main__':
    args = parse_args()
    main(dataset=args.dataset, track_number=args.track_number)
