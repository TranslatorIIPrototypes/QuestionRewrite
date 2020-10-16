[![Build Status](https://travis-ci.com/TranslatorIIPrototypes/QuestionRewrite.svg?branch=master)](https://travis-ci.com/TranslatorIIPrototypes/QuestionRewrite)

# Question Augmentation
### A web service and Swagger UI for the Question Augmentation service for ARAGORN.

This serivce accepts a [translator reasoner standard message](https://github.com/NCATS-Tangerine/NCATS-ReasonerStdAPI) containing a question graph and returns a set of similar questions that may yield better answers.

## Demonstration

A live version of the API can be found [here](https://questionaugmentation.renci.org/apidocs/).

An example notebook demonstrating the API can be found [here](https://github.com/TranslatorIIPrototypes/QuestionRewrite/blob/master/documentation/QuestionAugmentationSimilarity_strider.ipynb).

## Deployment

Please download and implement the Docker container located in the Docker hub repo: renciorg\qrw.

Kubernetes deployment files are available in the \kubernetes directory.

### Local Deployment

This environment expects Python version 3.8.

```bash
cd <code base>
pip install -r requirements.txt
python main.py --host 0.0.0.0 --port 6380
```

### Docker

```bash
docker run -it -p <port>:6380 QuestionAugmentation
```

### Kubernetes configurations
    kubernetes configurations and helm charts for this project can be found at: 
    
    https://github.com/helxplatform/translator-devops/question-rewrite
    
## Usage

http://"host name or IP":"port"/apidocs

