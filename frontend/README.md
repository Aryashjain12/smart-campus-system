# Smart Campus Intelligence System

An AI-powered real-time crowd monitoring system for campuses.

## Live Demo
https://smart-campus-system-1-d8ej.onrender.com

## Problem
Students waste time due to overcrowding in mess, library and admin office.

## Solution
Uses computer vision to detect crowd density in real-time and displays
it on a live dashboard — helping students avoid congested areas.

## Tech Stack
- AI/ML: YOLOv8 + OpenCV (person detection)
- Backend: Python + Flask (REST API)
- Frontend: React (live dashboard)
- Deployment: Render (free cloud hosting)

## Features
- Real-time people counting using AI
- Crowd status: Low / Medium / High
- Dashboard updates every 2 seconds
- Deployable on existing CCTV infrastructure

## How to Run Locally

### Backend
cd backend
pip install -r requirements.txt
python app.py

### Frontend
cd frontend
npm install
npm start

## Architecture
Camera → YOLOv8 detects people → Flask API → React Dashboard

## Future Scope
- Queue detection
- Peak hour prediction
- Mobile app
- Multi-camera support