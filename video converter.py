import imageio
import os
import cv2
import numpy as np

# Load the keywords and links from the text file into a dictionary
keywords_and_links = {}
with open("keyword.txt", "r") as file:
    for line in file:
        parts = line.strip().split(":")
        if len(parts) == 2:
            keyword, image_link = parts[0].strip(), parts[1].strip()
            keywords_and_links[keyword] = image_link

# Get user input as a sentence
user_input = input("Enter a sentence: ")

# Tokenize the sentence into keywords
selected_keywords = user_input.split()

selected_image_filenames = []

# Search for each keyword in the dictionary and add the corresponding image link to the list
for keyword in selected_keywords:
    if keyword in keywords_and_links:
        selected_image_filenames.append(keywords_and_links[keyword])
    else:  #print(f"Keyword not found: {keyword}")
        pass



# Output video file
output_video = "output.mp4"

# Frame dimensions
frame_width = 640
frame_height = 480

# Duration settings
image_duration = 3
transition_duration = 2

frame_durations = [image_duration] * len(selected_image_filenames)

for i in range(len(selected_image_filenames) - 1):
    frame_durations.insert(i * 2 + 1, transition_duration)

# Create the video writer
video_writer = imageio.get_writer(output_video, fps=1)

for i, image_filename in enumerate(selected_image_filenames):
    image = imageio.imread(image_filename)
    if image is not None:
        if image.shape[0] != frame_height or image.shape[1] != frame_width:
            image = cv2.resize(image, (frame_width, frame_height))

        for _ in range(int(frame_durations[i])):
            video_writer.append_data(image)

        if i < len(selected_image_filenames) - 1:
            next_image = cv2.resize(imageio.imread(selected_image_filenames[i + 1]), (frame_width, frame_height))
            for j in range(int(transition_duration)):
                alpha = 1.0 - j / transition_duration
                blended_frame = cv2.addWeighted(image, alpha, next_image, 1.0 - alpha, 0)
                video_writer.append_data(blended_frame)
    else:
        print(f"Unable to load image: {image_filename}")

video_writer.close()

print("Video created successfully.")
