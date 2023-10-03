# Marshallyin.com Parser

This project is a web scraping tool that parses data from [marshallyin.com](https://www.marshallyin.com/) using Scrapy and runs in a Docker container. It allows you to scrape and collect various data from the website efficiently.

## Prerequisites

Before using this parser, make sure you have the following software installed on your system:

- [Docker](https://www.docker.com/)

## Usage with Docker

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/marshallyin.com-parser.git
2. Navigate to the project directory:
   ```bash
   cd marshallyin.com-parser
3. Build the Docker image:
   ```bash
   docker build -t marshallyin-parser .
4. Create a Docker volume for the data storage:
   ```bash
   docker volume create marshallyin-data
5. Run the Docker container with the volume mapping:
   ```bash
   docker run -it --name marshallyin-parser-container -v marshallyin-data:/app/data marshallyin-parser
- The -v flag is used to create a volume and map it to the app/marshallyin/data directory inside the container.
- The marshallyin-data volume name can be customized to your preference.
6. The parser will start and begin scraping data from marshallyin.com. The scraped data will be stored in the Docker volume.
7. To access the scraped data on your local machine, you can use the docker cp command to copy the data from the Docker volume to a local directory:
   ```bash
   docker cp marshallyin-parser-container:/app/data /path/on/your/local/machine

- Replace /path/on/your/local/machine with the desired local directory path.
8. To stop and remove the container when you're done:
   ```bash
   docker stop marshallyin-parser-container
   docker rm marshallyin-parser-container
## Note (Alternative launch)
If you want to get only specific kind of lessons you can run container using the following command:
   ```bash
   docker run -it --name marshallyin-parser-container -v marshallyin-data:/app/marshallyin/data marshallyin-parser /bin/sh -c "cd marshallyin && scrapy crawl <Spider_name>"
   ```
<Spider_name> should be replaced with one of the following:
1) AlphabetJP 
2) GrammarJP
3) KanjiJP
4) VocabularyJP
### Note
Each of them corresponds to their respective lesson names.