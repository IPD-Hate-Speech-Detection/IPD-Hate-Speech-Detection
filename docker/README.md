# Trial Deployment

## Setup

Instructions on how to set up the project.

1. Clone the repository:

   ```sh
   git clone https://github.com/Tirath5504/IPD-Hate-Speech-Detection.git
   cd docker/app
   ```

2. Build and run the Docker containers:
   ```sh
   docker build -t hate_speech_app .
   docker run -p 5000:5000 hate_speech_app
   ```

## Testing

Instructions on how to run the tests.

1. Run the tests with the following command:
   ```sh
   cd ..
   python -m unittest test_server.py
   ```
