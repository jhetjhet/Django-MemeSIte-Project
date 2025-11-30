# Meme Site – Django Social Media Platform

A full-featured social media web application built with Django, where users can share memes, ideas, and content through images and text. All posts are publicly visible, and users can interact through likes, dislikes, and comments with real-time updates.

## 🎯 Overview

This project demonstrates a complete Django web application with real-time features, production-ready deployment, and clean architecture. It's perfect for learning Django fundamentals, WebSocket integration, and Docker containerization.

## 🖼️ Screenshots

<img width="447" height="796" alt="Screenshot 2025-12-01 002922" src="https://github.com/user-attachments/assets/77f1437b-5c2a-472e-821d-1d386b5787d0" />

<img width="1415" height="906" alt="Screenshot 2025-12-01 004836" src="https://github.com/user-attachments/assets/1703d596-73f6-41b8-bd25-d53313303876" />

<img width="1420" height="908" alt="Screenshot 2025-12-01 004904" src="https://github.com/user-attachments/assets/edab70b5-ac30-45cd-96b8-8921c2665736" />

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Django 3.0.8 |
| **Database & ORM** | Django ORM with migrations |
| **Frontend** | Django Templates + Bootstrap |
| **Real-time Updates** | Django Channels (WebSocket) + Redis |
| **Production Server** | Gunicorn + Nginx |
| **Containerization** | Docker & Docker Compose |

## ✨ Key Features

- **User Authentication** – Registration, login, and minimal profile management
- **Post Creation & Sharing** – Share images and text-based content
- **Social Interactions** – Like, dislike, and comment on posts in real-time
- **User Profiles** – View user profiles, follow/unfollow functionality
- **Live Updates** – WebSocket-powered real-time notifications for:
  - Post deletions
  - Likes and dislikes
  - New comments and removed comments
- **Search Functionality** – Search and discover users
- **Responsive Design** – Mobile-friendly interface with Bootstrap

## 📋 Requirements

- **Docker** and **Docker Compose** (for containerized deployment)
- Alternatively: Python 3.9+, PostgreSQL/MySQL, Redis (for local development)

## 🚀 Quick Start

### Development Mode
```bash
docker compose -f docker-compose-dev.yml up
```
Runs the development server with hot-reload enabled.

Access the application at `http://localhost:8000`

### Production Mode
```bash
docker compose up
```
Runs the production environment with Gunicorn and Nginx.

Access the application at `http://localhost`

