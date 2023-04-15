# Video Searcher
__Short Description:__ A tool that allows its users to upload .mp4 videos that
will be displayed in a gallery. The backend will generate subtitles for these
videos and make them searchable with Atlas Search.

---
## Description

The application consists of a React Frontend and a rudimentary python Flask
backend. The frontend allows the users to select videos and upload them. The
uploaded videos are then shown in a Gallery View, with the possibility to
search for content in the videos, show the relevant segments and make it
possible to jump to them.

The backend handles serving of the static files and videos, as well as
communication with the MongoDB database. As soon as a video is uploaded,
OpenAI Whisper is used to generate its subtitles in a separate process. As
soon as they are done, they are uploaded to MongoDB, where they will be able
to be read back.

The MongoDB database consists of two collections. The ``videos`` collection
stores the video titles, paths to the .mp4 files on disk, as well as the whole
subtitle as text to make it searchable. The ``segments`` collection contains
the individual segments that have been identified in the subtitles and the
text within. They are searchable as well and can be used to filter inside a
single video for the relevant segments containing a certain topic.

---
## Setup

__1. Configure Laptop__

* Ensure Node and NPM are installed your laptop
* Ensure Python version >=3.10 is installed (Might work with older versions as
  well, however this wasn't tested)
* Ensure that you have a running cluster in MongoDB Atlas (M0 will suffice)
  and the rights to create Search Indexes on it

__2. Build the frontend__

The frontend is located in the ``frontend`` folder and is built using npm. In
order to compile a production build, the following needs to be executed:

```bash
cd frontend
npm install
npm run build
```

In order to simply debug the application and running it on your machine
locally, you can also issue:

```bash
npm run start
```

to let it run on ``localhost:3000``. This will not be able to directly talk to
the backend however, since this will be running on a different port.
Therefore, database access will not be possible and the available videos and
segments will not be showing.

__3. Configure the backend__

The backend is located in the ``backend`` folder and uses python and Flask to
serve the static files and videos, as well as manage the database
communication.

The folder contains a ``requirements.txt`` file that contains all of the
Python dependencies that are needed. The easiest way to install them will be
in a virtual environment like the following:

```bash
python3 -m venv venv
. ./venv/bin/activate
pip3 install -r requirements.txt
```

In order to run properly, the openai-whisper module will require ffmpeg to be
installed on the system as well. A full setup description for this is
available at https://github.com/openai/whisper.

The backend is configured through a file called ``config.py``, which needs to
be created. A template is available at ``config.template.py`` and can be
copied for this. It contains the following configuration parameters:

* ``MONGO_URL`` - URL of the cluster that is going to be used, including
    username and password
* ``MONGO_DB`` - The database that will be used to store all of the
    application data. The default can be left as-is.
* ``FRONTEND_PATH`` - The path where the production build of the frontend is
    located at. The default value will work, if the backend is running locally
    and the frontend was built as described earlier.

After this, the backend can be served at ``localhost:5050`` with the following
command:

```bash
python3 -m flask --app main run --host 0.0.0.0 --port 5050
```

__4. Create the Search Indexes__

The search indexes being used are very basic, one for each of the collections.
The JSON representation of the search indexes is simply the following:

```JSON
{
  "mappings": {
    "dynamic": true
  }
}
```

When navigating to the search tab of the cluster in Atlas, the indexes can be
created by pressing Create Index. After selecting the database and collections
(by default ``videoSearcher.videos`` and ``videoSearcher.segments``), the
index can be created by pasting the JSON from earlier into the JSON editor or
selecting the default options in the visual editor.

After this, the application should be fully functional and can be accessed at
``localhost:5050``.
