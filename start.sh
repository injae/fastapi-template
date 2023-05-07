#!/bin/bash
cd src && poetry run uvicorn server.app:create_app --reload --factory
