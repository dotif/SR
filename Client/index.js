function get_user_profile(done){
    const results = fetch("http://127.0.0.1:8800/user_profile/")
    results
        .then(response => response.json())
        .then(data => { done(data)
        });
};

function get_user_movies(user_id, done){
    const results = fetch(new URL(user_id,"http://127.0.0.1:8800/user_movies/"))
    results
        .then(response => response.json())
        .then(data => { done(data)
        });
};

function get_recomendacion(done){
    const results = fetch("http://127.0.0.1:8800/recomendar/")
    results
        .then(response => response.json())
        .then(data => { done(data)
        });
};


$("#search").keypress(function(event) {
    if (event.keyCode === 13) {
        //const test = document.querySelector("#usr_mvs");
        
        var user_id = $("#search").val();
        $("#response").empty();
        $("#error").empty();
        get_user_movies(user_id,data => {              
            const user_movies = document.querySelector("#user_movies");
            user_movies.append("Peliculas calificadas por el usuario")
            const obj = JSON.parse(data);
            const tbody = document.querySelector("#response_um");    
            Object.keys(obj).forEach(function(key) {
                const tr = document.createElement('tr');
                const th_movie_id = document.createElement('th');
                const td_title = document.createElement('td');
                const td_rating = document.createElement('td');
                const td_genres = document.createElement('td');                                            
                td_genres.append(obj[key].genres);
                td_rating.append(obj[key].rating);
                td_title.append(obj[key].title);
                th_movie_id.append(obj[key].movie_id);                
                tr.append(th_movie_id);
                tr.append(td_title);
                tr.append(td_genres);
                tr.append(td_rating);
                tbody.append(tr);
            });                                                                    
        });

        get_user_profile(data => {
            const user_profile = document.querySelector("#user_profile");
            user_profile.append("Perfil de Usuario")
            const obj = JSON.parse(data);            
            const tbody = document.querySelector("#response_up");    
            Object.keys(obj).forEach(function(key) {
                const tr = document.createElement('tr');
                const th_generes = document.createElement('th');
                const td_pond = document.createElement('td');                
                th_generes.append(key)
                td_pond.append(obj[key]);                
                tr.append(th_generes);
                tr.append(td_pond);                
                tbody.append(tr);
            });
        });

        get_recomendacion(data => {
            const user_profile = document.querySelector("#recomendacion");
            user_profile.append("Recomendaciones")
            const obj = JSON.parse(data);    
            console.log(data)       
            const tbody = document.querySelector("#rec");    
            Object.keys(obj).forEach(function(key) {
                const tr = document.createElement('tr');
                const th_movie_id = document.createElement('th');
                const td_title = document.createElement('td');
                const td_rating = document.createElement('td');
                const td_genres = document.createElement('td');                                            
                td_genres.append(obj[key].genres);
                td_rating.append(obj[key]["0"]);
                td_title.append(obj[key].title);
                th_movie_id.append(obj[key].movie_id);                
                tr.append(th_movie_id);
                tr.append(td_title);
                tr.append(td_genres);
                tr.append(td_rating);
                tbody.append(tr);
            });                              

        });
    }
});

