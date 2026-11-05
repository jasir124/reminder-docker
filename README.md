# Event Reminder CRUD Application

This mini-project demonstrates how to create, read, update, and delete events in a Flask application running in Docker. SQLite stores the events in a Docker volume.

## Technologies

HTML, CSS, Python Flask, SQLite, Docker, Git, and GitHub.

## CRUD operations

| Operation | Route | How to try it |
| --- | --- | --- |
| Create | POST /add | Enter Project Demo, 10 November 2026, and Docker demonstration. Select Add Event. |
| Read | GET / | Find Project Demo in the Saved Events table. |
| Update | GET and POST /edit/<id> | Select Edit, change the description, and save. |
| Delete | POST /delete/<id> | Select Delete and confirm. Check that the row disappears. |

The application creates the SQLite database and table at startup. Add demo events through the form.

## Project structure

- `app.py` contains the Flask routes and SQLite queries.
- `templates/` contains the homepage and edit page.
- `static/style.css` contains the page styles.
- `requirements.txt` lists the Python dependency.
- `Dockerfile` and `docker-compose.yml` configure the container.
- `data/` holds the local SQLite database.
- `screenshots/` holds screenshots of the demonstration.

## Build and run

Start Docker Desktop or your Docker engine, then run these commands from the project folder.

```sh
docker build -t event-reminder .
docker run -d --name event-reminder-container -p 8080:8080 -v event-reminder-data:/app/data event-reminder
docker ps
docker logs event-reminder-container
```

Open [Event Reminder](http://localhost:8080). Docker maps port 8080 on your computer to port 8080 in the container.

You can also start the same setup with `docker compose up --build -d`. Use one startup method at a time because both use the same container name and port.

To verify persistence, add an event, refresh the page, and run `docker restart event-reminder-container`. Refresh again and check that the event is still there. The database lives in the named volume `event-reminder-data`.

Stop the container with `docker stop event-reminder-container`. To start it again, run `docker start event-reminder-container`.

## Screenshots

Capture these after starting the container and save them in `screenshots/`.

| File | Capture |
| --- | --- |
| 01-homepage.png | Homepage at localhost:8080 |
| 02-add-event.png | Saved Events table after adding Project Demo |
| 03-edit-event.png | Prefilled Edit Event page |
| 04-delete-event.png | Saved Events table after confirming deletion |
| 05-docker-image.png | Image shown by `docker image ls event-reminder` |
| 06-docker-container.png | Running container shown by `docker ps` |
| 07-docker-terminal.png | Terminal showing the successful build and run commands |

## GitHub

Repository link pending publication.

## Conclusion

Flask receives the form submissions and uses SQLite to save changes. Docker packages the application, and the named volume keeps events available across container restarts.
