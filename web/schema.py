instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS perfil;',
    'DROP TABLE IF EXISTS user;',
    'DROP TABLE IF EXISTS instrumento;',
    'SET FOREIGN_KEY_CHECKS=1;',
        """
        CREATE TABLE perfil (
            id_perfil INT PRIMARY KEY AUTO_INCREMENT,
            perfil VARCHAR(50) NOT NULL
    ); 
    """,
    """
        CREATE TABLE user (
            id_user INT PRIMARY KEY AUTO_INCREMENT,
            create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50) NOT NULL,
            correo VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL,
            id_perfil INT NOT NULL,
            FOREIGN KEY (id_perfil) REFERENCES perfil(id_perfil)

    );
    """,
    """
        CREATE TABLE instrumento (
            id_instrumento INT PRIMARY KEY AUTO_INCREMENT,
            create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            tipo_instrumento VARCHAR(50) NOT NULL,
            marca VARCHAR(100) NOT NULL,
            nombre VARCHAR(100) NOT NULL,
            nro_serie VARCHAR(100) NOT NULL,
            codigo VARCHAR(50) NOT NULL,
            valor DECIMAL(10, 2) NOT NULL,
            cantidad INT NOT NULL,
            stock BOOLEAN NOT NULL
    );  
    """
]