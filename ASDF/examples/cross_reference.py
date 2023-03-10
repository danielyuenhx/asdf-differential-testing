import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

import sys
sys.path.append("../")
import utils
from crossasr import CrossASR
from crossasr.text import Text

if __name__ == "__main__":
    
    config = utils.readJson(sys.argv[1]) # read json configuration file

    tts = utils.getTTS(config["tts"])
    asrs = utils.getASRS(config["asrs"])
    
    crossasr = CrossASR(tts=tts, asrs=asrs, output_dir=config["output_dir"], recompute=True)

    text = "software engineering conference"
    filename = "software_engineering_conference"

    crossasr.processText(Text(filename, text))
    crossasr.printResult(text=text, filename=filename)
