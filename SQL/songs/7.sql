SELECT AVG(energy) FROM songs WHERE artist_id = (SELECT id FROM artists WHERE NAME = "Drake");

