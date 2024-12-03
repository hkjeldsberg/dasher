#! /usr/bin/env bash

isort app tests

black app tests

flake8 app tests
