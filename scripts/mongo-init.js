db.createUser(
    {
        user: "image_search",
        pwd: "image_search_password",
        roles: [
            {
                role: "readWrite",
                db: "image_search"
            }
        ]
    }
);

