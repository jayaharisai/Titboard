<p align="center">
  <img src="assets/logo.png" alt="Titboard Logo" width="200" />
</p>

<h1 align="center">Titboard</h1>

<p align="center">
  The app which helps in your daily work flow
</p>

## 📦 Clone and Run with Docker

### Step 1: Clone the Repository

```bash
git clone https://github.com/jayaharisai/Titboard.git
cd Titboard
```

### Step 2: Build the Docker Image

```bash
sudo docker build -t titboard .
```
### Step 3: Run the Docker Container
```bash
sudo docker run -d -p 8000:8000 titboard