# microsoft-cv-cli
Welcome to the RapidAPI Microsoft Computer Vision CLI, a robust command-line interface powered by Microsoft's Computer Vision API through RapidAPI. This tool allows you to seamlessly integrate advanced image analysis and recognition features into your workflow directly from the terminal.

A Python script that uses the Microsoft Azure Computer Vision API to perform various image analysis tasks such as analyzing images, describing images, detecting objects, using specific models, performing optical character recognition (OCR), generating thumbnails, and identifying areas of interest in an image.


# Prerequisites
- Python 3.x
- Requests package
- A Computer Vision API subscription key (set in config.json)


# Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Configure the project by adding `YOUR_RAPIDAPI_KEY` in `config.json`.

# Usage
The script can be used from the command line by passing arguments to specify the function to call and the parameters.


# Functions
The following functions from the API are supported:

- **Analyze Image**  
  `python main.py --analyze <image_url>`

  Extract visual features, categories, tags, descriptions, faces, etc.

- **Describe Image**  
  `python main.py --describe <image_url> --count 3`

  Generate a description of the image in human readable language.

- **Detect Objects**  
  `python main.py --detect <image_url>`
  
  Detect common objects in an image.
  
- **Use Recognition Model**
  `python main.py --models <image_url> --use landmarks`

  Specify a domain-specific model to recognize particular classes of images.
  
- **OCR**  
  `python main.py --ocr <image_url>`
  
  Extract printed text in an image using Optical Character Recognition.
  
- **Generate Tags**
  `python main.py --tag <image_url>`

  Generate tags based on image content.
  
- **Generate Thumbnail**  
  `python main.py --thumbnail <image_url> --width 100 --height 100`

  Generate a thumbnail image with customizable dimensions.

See the script code or `--help` for more details on arguments and options available for each function.

# Example
python main.py --analyze "https://example.com/images/cat.jpg"
