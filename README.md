# Setup Instructions

1. **Copy and Configure Environment File**  
   Duplicate the `.env.sample` file and rename it to `.env`. Open the `.env` file and adjust the configuration settings as needed.

2. **Install Docker**  
   Ensure Docker is installed on your machine. If it's not already installed, you can download and install it from the [official Docker website](https://www.docker.com/products/docker-desktop).

3. **Clone the Repository**  
   Clone this repository to your preferred location using the following command:
   ```bash
   git clone git@github.com:ln2khanal/fastapi.git
   
4. **Navigate to the Project Directory**
   Change to the project directory with: `cd fastapi`
   
6. **Build and Run the Services**
   Use Docker Compose to build and start the services: `docker compose up --build`
   
7. **Browse the HTML page**
   Navigate to the landing page @ `http://localhost` & Swaggar APIs @ `http://localhost/docs`

8. **Upload your data**
   Using `/api/v1/datasource/add` api, upload your data. You can upload sample data included in this repo @ `sampledata.xlsx`.

# Potential tasks in the backlog:

1. **TestCase addition**
2. **Authorization Token implementation**
3. **File data structure validation**
