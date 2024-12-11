from glob import glob
import pandas as pd

def load_subtitles_dataset(dataset_path):
    subtitles_path = glob(dataset_path + '/*.ass')
    
    scripts = []
    episode_nums = []
    
    for path in subtitles_path:
        
        #Read lines
        with open(path, 'r') as file:
            lines = file.readlines()
            lines = lines[26:]
            lines = [",".join(line.split(",")[9:]) for line in lines]
            
        lines = [line.replace("\\N","") for line in lines]
        script = " ".join(lines)
        
        episode = int(path.split("\\")[-1].split(".")[0])
        
        scripts.append(script)
        episode_nums.append(episode)
        
    
    df = pd.DataFrame.from_dict({"episode": episode_nums, "script": scripts})
    
    return df