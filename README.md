# PoliticCrawler

PoliticCrawler is an application designed to analyze political content from social media platforms.
It aggregates data
from various political channels, categorizes them by political parties or along a left-right spectrum, generates
transcripts of the content, and uses AI to analyze and classify the content into specific categories.
Additionally,
it features a web-based user interface for data visualization and administrative tasks, and implements a distributed
system to efficiently manage API call limitations.

## Features
- **Data Aggregation**: Collects content from political channels across multiple social media platforms.
- **Categorization**: Assigns content to specific political parties or positions it on a left-right political spectrum.
- **Transcription**: Converts audio and video content into text transcripts for detailed analysis.
- **AI Analysis**: Employs artificial intelligence to analyze transcripts and categorize content based on themes,
  sentiment, and other relevant metrics.
- **Web Interface**: Provides a user-friendly web UI to visualize data through graphs and charts, and includes
  administrative pages for managing channels and system settings.
- **Distributed System**: Implements a distributed architecture to manage API call limitations by allowing multiple
  contributors to update channel data without exposing database credentials.

## Installation (Developer Setup)

### Prerequisites

- [Docker](https://www.docker.com/) installed on your system.
- [Node.js](https://nodejs.org/) installed.
- [Python](https://www.python.org/) installed.

### Steps

1. **Clone the Repository**:

```bash
git clone https://github.com/Klausmp/politiccrawler.git
cd politiccrawler
```

2. **Set Up the Environment Variables**:

```bash
cp example.env .env
```

3. **Install the Dependencies**:
```bash
npm install
```

4. **Build the Docker Containers**:
   This command will start the necessary services, including the PostgresSQL database.

```bash
docker-compose up -d
```

5. **Run the Migrations and Seed the DB**:
   This command will create the necessary tables in the database. This will also seed the database with some initial data.

```bash
npm run db-migrate-and-seed
```

6. **Start the Application**:
   This command will start the backend server and the frontend development server.

```bash
npm run dev
``` 

7. **Access the Application**:
   Open your browser and navigate to `http://localhost:3000`.

License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.


