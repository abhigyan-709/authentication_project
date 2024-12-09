# This readme defines the documentation of the CICD for  the realtime showcase of application deploument 

## Techstack Used:
1. Python - FastAPI : For the API Development 
2. Docker - Dockerfile for Custom App Image 
          - Docker Compose file for mongodb image and to manage multicontainer application 
3. AWS ECR - Image Storage 
4. AWS EKS - For kubernetes cluster & pods
5. GitHub - For socurce code management
6. GitHub Actions - For ci/cd 
7. Infrastructure Management & provisioning 


Steps: 
- Prepare the Application
    - Application will be prepared through the FasAPI RestAPI framework
    - Test in Local machine directly or in Virtual env (see main readme file to prepare teh app in Virtual env)
    - Write docker file (see the /app/Dockerfile for the current application repo)
    - bind the image for the FastAPI - 
    bash
    ```
    docker build -t app_name:tag .
    ``` 