db.taxi_rides.aggregate([
    {
        $match: { "client_review.rating": { $ne: null } }
    },
    {
        $group: {
            _id: "$driver_id",
            avgRating: { $avg: "$client_review.rating" }
        },

    },
    {
        $match: { "avgRating": { $lt: 3.5 } }
    },

])