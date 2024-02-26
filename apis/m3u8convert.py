import os

# Update the file path in the m3u8 playlist
def __rewrite_file_paths(f):
    print('Processing ' + f)
    file_contents = open(f).read()
    lines = file_contents.split('\n')
    new_lines = []
    for line in lines:
        if line.startswith('file://'):
            new_line = 'file://' + os.path.join(os.getcwd(), os.path.sep.join(line.split('/')[-2:]))
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    open(f, 'w').write('\n'.join(new_lines))


# Run the ffmpeg command to convert the file
def __covert_m3u8_file_to_mp4(f): 
    command = ''.join(['ffmpeg -i "', f, '" -c:v libx264 -preset slow -crf 23 -c:a copy "', f.replace('.m3u8', '.mp4'), '"'])
    # print('Running command "' + command + '"')
    os.system(command)

# Perform the conversion for all files in the current directory
def convert_m3u8_files(f):
    __rewrite_file_paths(f)
    __covert_m3u8_file_to_mp4(f)
