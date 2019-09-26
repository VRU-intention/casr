#create the images from videos


mkdir images
for file in videos/*.mp4
do

# check was the video extracted before, if yes, jump to next video
# remember to delete the corresponding images folder if it is not fully extracted
if [ -d ${file} ]; then
continue;
fi

filename=$(basename "$file")
fname="${filename%.*}"
echo "processing the video of " $fname

# create a folder corresponding to the processed video for saving images
mkdir images/$fname

ffmpeg -i $file -f image2 -qscale 1 images/$fname/frame_%05d.png

echo "finish and saved the extracted images of " $fname
done
