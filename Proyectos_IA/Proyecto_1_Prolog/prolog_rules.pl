% Recomendar un libro con la categoría
recommend_book(User, RecommendedBook) :-
    sale(User, BoughtBook),
    book_category(BoughtBook, Category),
    book_category(RecommendedBook, Category),
    BoughtBook \= RecommendedBook, % Esto hace que no recomiende el mismo libro
    \+ sale(User, RecommendedBook). % Esto hace que no recomiende un libro que ya compró el usuario
 
% Recomendar una lista de libros
recommend_list(User, BookList) :-
    findall(RecommendedBook, recommend_book(User, RecommendedBook), BookList). %  Usa la regla anterior para hacer una lista de todos los libros recomendados
    
% Encontrar usuarios con gustos similares
similar_users(User, SimilarUser) :-
    sale(User, Book),
    sale(SimilarUser, Book),
    User \= SimilarUser. % Esto hace que no se recomiende el mismo usuario
    