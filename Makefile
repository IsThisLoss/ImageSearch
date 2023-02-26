run-docker:
	docker-compose up -d --build

start-dev-env:
	cd dev && docker-compose up -d

down-dev-env:
	cd dev && docker-compose down

run-backend:
	cd backend && uvicorn image_search:app --reload

run-frontend:
	cd frontend && yarn run serve
