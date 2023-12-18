SELECT ROUND(AVG(SCORE), 1) AS "Average Score", MOVIE.MOVIENAME AS "Movie Name", MOVIE.GENRE AS "Genre", MOVIE.RUNTIME AS "Runtime", MOVIE.RELEASEDATE AS "Release Date" FROM REVIEW
JOIN MOVIE ON REVIEW.MOVIEID = MOVIE.MOVIEID
GROUP BY MOVIE.MOVIENAME, MOVIE.GENRE, MOVIE.RUNTIME, MOVIE.RELEASEDATE
ORDER BY "Average Score" DESC; 