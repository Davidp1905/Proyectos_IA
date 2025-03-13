% ****************  QUERY #1  ****************
% Recomendar un libro con la categoría
recommend_book(User, RecommendedBook) :-
    sale(User, BoughtBook),
    book_category(BoughtBook, Category),
    book_category(RecommendedBook, Category),
    BoughtBook \= RecommendedBook, % Esto hace que no recomiende el mismo libro
    \+ sale(User, RecommendedBook). % Esto hace que no recomiende un libro que ya compró el usuario
 
% ****************  QUERY #2  **************** 
% Recomendar una lista de libros
recommend_list(User, BookList) :-
    findall(RecommendedBook, recommend_book(User, RecommendedBook), BookList). %  Usa la regla anterior para hacer una lista de todos los libros recomendados
    
% ****************  QUERY #3  ****************
% prueba con rodrigo, ana y lucas
% Encuentra libros recomendados en base a gustos similares de manera recursiva
recomendar_recurrente(User, Recomendaciones) :-
    findall(Book, (sale(User, Book), rating(User, Book, Rating), Rating >= 3), LikedBooks), % Encuentra libros que el usuario ha calificado con 4 o más
    recomendar_recursivo(User, LikedBooks, [], Recomendaciones).  % Llama a la recursión

% Caso base: Cuando no hay más libros por recomendar, se devuelve la lista acumulada.
recomendar_recursivo(_, [], Recs, Recs).

% Caso recursivo: Busca otro usuario con gustos similares y recomienda libros nuevos
recomendar_recursivo(User, [LikedBook | Rest], Acumulado, Recomendaciones) :-
    sale(OtherUser, LikedBook),                % Encuentra otro usuario que haya comprado el mismo libro
    rating(OtherUser, LikedBook, OtherRating), % Obtiene la calificación del otro usuario
    OtherUser \= User,                         % Asegura que no sea el mismo usuario
    OtherRating >= 3,                          % Filtra solo si el otro usuario lo calificó alto

    sale(OtherUser, BookRecomendado),          % Encuentra otro libro que el usuario 2 haya comprado
    rating(OtherUser, BookRecomendado, Rating2), % Obtiene su calificación
    Rating2 > 3,                               % Filtra solo libros con calificación mayor a 3
    \+ sale(User, BookRecomendado),            % Asegura que User no haya comprado ya ese libro
    \+ member(BookRecomendado, Acumulado),     % Evita libros repetidos en la lista

    append(Acumulado, [BookRecomendado], NuevoAcumulado), % Agrega el libro a la lista de recomendaciones
    recomendar_recursivo(User, Rest, NuevoAcumulado, Recomendaciones). % Continúa la recursión con los libros restantes


% ****************  QUERY #4  ****************
% tienen mas de 10: andres, carolina, martin
% no tiene ninguno: santiago
%top_10_favoritos([andres, luis, karen], TopLibros).
top_10_favoritos(Users, Resultados) :-
    findall(User-TopBooks, (  % Encuentra la lista de favoritos para cada usuario
        member(User, Users),   % Itera sobre cada usuario en la lista "Users"
        
        % Obtiene todos los libros calificados por el usuario con rating > 3
        findall(Book-Rating, (
            rating(User, Book, Rating),
            Rating > 3  % Filtra solo libros con calificación mayor a 3
        ), BooksWithRatings),

        % Ordena los libros por calificación de mayor a menor
        sort(2, @>=, BooksWithRatings, SortedBooks),

        % Extrae solo los primeros 10 libros de la lista ordenada
        extract_books(SortedBooks, 10, TopBooks)
    ), Resultados).

% Regla auxiliar: Extrae los primeros N libros de la lista.
% Cuando N llega a 0, se devuelve una lista vacía.
extract_books(_, 0, []). 

% Si la lista de libros está vacía antes de llegar a N, se devuelve una lista vacía.
extract_books([], _, []). 

% Caso recursivo: Se toma el primer libro de la lista y se reduce N en 1.
extract_books([Book-_|T], N, [Book|R]) :-
    N > 0,
    N1 is N - 1,
    extract_books(T, N1, R).

% ****************  QUERIES VARIAS  ****************

% Encontrar libros con rating mayor a 3
top_books(BookList) :-
    findall(Book, rating(_, Book, Rating), Books),
    findall(Book-Rating, (member(Book, Books), Rating > 3), BookList).

    % Encontrar usuarios con gustos similares
similar_users(User, SimilarUser) :-
    sale(User, Book),
    sale(SimilarUser, Book),
    User \= SimilarUser. % Esto hace que no se recomiende el mismo usuario
