import os
import re

class PT_CSVStyler:

    def __init__(self):
        pass

    @staticmethod
    def load_styles(stylesCSV):

        stylesDict={}

        if not os.path.exists(stylesCSV):
            print(f"PT.CSVStyler: Error! No styles.csv found. Put styles.csv in the root directory of ComfyUI.")
            return stylesDict

        try:
            with open(stylesCSV, 'r', encoding="utf-8") as f:
                lines = f.readlines()

            styles=[]

            for line in lines[1:]:
                styles.append( re.split(',(?=(?:[^"]*"[^"]*")*[^"]*$)', line.rstrip('\n')) )    # line parser

            stylesDict = {item[0]: item[1:] for item in styles}         # list -> dict   

        except Exception as ex:
            print(f"PT.CSVStyler: Error loading styles.csv. Error: {ex}")

        return stylesDict
    
    @staticmethod
    def style_processor(style, prompt):
        key_word = '{prompt}'                   # style may contain {prompt}, wich should be replaced with actual prompt

        if style:                               # style is empty ?
            if key_word in style:
                processedPrompt = style.replace(key_word, prompt)
            else:
                if prompt:
                    processedPrompt = f'{style}, {prompt}'      # extra comma after style definition, mb unnecessary
                else:
                    processedPrompt = f'{style}'                # if prompt empty pass only style field
        else:
            processedPrompt = prompt

        return processedPrompt

    @classmethod
    def INPUT_TYPES(cls):
        cls.stylesList = cls.load_styles(os.getcwd() + "\\styles.csv")

        return {
            "required": {
                "styles": (list(cls.stylesList.keys()),),
                "bypass_mode": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Bypass processing"}),
                "positive": ("STRING", {
                    "multiline": True,
                    "tooltip": "Positive prompt"
                }),
                "negative": ("STRING", {
                    "multiline": True,
                    "tooltip": "Negative prompt"
                }),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive", "negative")

    FUNCTION = "process"

    CATEGORY = "conditioning"

    DESCRIPTION = """
    Process prompts according to selected style
    
    Settings:
    - bypass_mode: Bypass processing (pass input unchanged)
    """

    def process(self, styles, bypass_mode, positive, negative):

        stylePositive = self.stylesList[styles][0].strip('"')
        styleNegative = self.stylesList[styles][1].strip('"')

        if not bypass_mode:
            processedPositive = self.style_processor(stylePositive, positive)
            processedNegative = self.style_processor(styleNegative, negative)

        else:
            processedPositive = positive
            processedNegative = negative

        print(f'PT.CSVStyler: Processing...\n\
            Style Positive -> {stylePositive}\n\
            Style Negative -> {styleNegative}\n\
            Inbound Positive -> {positive}\n\
            Inbound Negative -> {negative}\n\
            Outbound Positive -> {processedPositive}\n\
            Outbound Negative -> {processedNegative}')

        return (processedPositive, processedNegative)
        