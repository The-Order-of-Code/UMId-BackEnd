-- Povoamento Da Nossa BD

USE easyid;

DELIMITER //

CREATE PROCEDURE `UserStudent`()
BEGIN

	-- Declare variables
	DECLARE v_finished INTEGER DEFAULT 0;
    DECLARE v_idAluno INT;
	DECLARE v_nome VARCHAR(45);
    DECLARE v_apelido VARCHAR(45);
    DECLARE v_email VARCHAR(45);
    DECLARE v_data_nascimento DATE;
    DECLARE v_numero INT;
    DECLARE v_ano_inscricao DATE;
    DECLARE v_ano_inscrito INT;
	DECLARE v_idCurso INT;

	-- Declare cursor for userstudent
	DECLARE cursor_userstudent CURSOR FOR 
	SELECT idAluno, nome, apelido, email, data_nascimento, numero, ano_inscricao, ano_inscrito, idCurso FROM fu.aluno;
 
	-- Declare NOT FOUND handler
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_finished = 1;
 
	OPEN cursor_userstudent;
 
	get_userstudent: LOOP
 
	FETCH cursor_userstudent INTO v_idAluno, v_nome, v_apelido, v_email, v_data_nascimento, v_numero, v_ano_inscricao, v_ano_inscrito, v_idCurso;
 
	IF v_finished = 1 THEN 
		LEAVE get_userstudent;
	END IF;
 
	-- Preencher User
    INSERT INTO easyid.general_user(`password`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `fullName`, `birthDate`, `birthParish`, `birthMunicipality`, `birthDistrict`, `birthCountry`)
    VALUES ('password', 0, CONVERT(v_idAluno,CHAR), v_nome, v_apelido, v_email, 1, 0, '2020-01-01 20:00:00', CONCAT(v_nome,CONCAT(" ",v_apelido)), v_data_nascimento, 'birthParish', 'birthMunicipality', 'birthDistrict', 'birthCountry');
	
    -- Preencher Student
    INSERT INTO easyid.general_student (`user_id`, `number`, `year`, `academicYear`, `edition`, `specialStatuses`, `studyPlan`, `course_id`)
    VALUES (LAST_INSERT_ID(), v_numero, YEAR(v_ano_inscricao), v_ano_inscrito, 0, 'specialStatuses', 'studyPlan', v_idCurso);
    
    COMMIT;
 
	END LOOP get_userstudent;
 
	CLOSE cursor_userstudent;
 
END //
 
DELIMITER ;

DELIMITER //

CREATE PROCEDURE `UserEmployee`()
BEGIN

	-- Declare variables
	DECLARE v_finished INTEGER DEFAULT 0;
    DECLARE v_idFuncionario INT;
	DECLARE v_nome VARCHAR(45);
    DECLARE v_apelido VARCHAR(45);
    DECLARE v_email VARCHAR(45);
    DECLARE v_data_nascimento DATE;

	-- Declare cursor for useremployee
	DECLARE cursor_useremployee CURSOR FOR 
	SELECT (idFuncionario+(SELECT MAX(id) FROM easyid.general_user)), nome, apelido, email, data_nascimento FROM fu.funcionario;
 
	-- Declare NOT FOUND handler
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_finished = 1;
 
	OPEN cursor_useremployee;
 
	get_useremployee: LOOP
 
	FETCH cursor_useremployee INTO v_idFuncionario, v_nome, v_apelido, v_email, v_data_nascimento;
 
	IF v_finished = 1 THEN 
		LEAVE get_useremployee;
	END IF;
 
	-- Preencher User
    INSERT INTO easyid.general_user(`password`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `fullName`, `birthDate`, `birthParish`, `birthMunicipality`, `birthDistrict`, `birthCountry`)
    VALUES ('password', 0, CONVERT(v_idFuncionario,CHAR), v_nome, v_apelido, v_email, 0, 0, '2020-01-01 20:00:00', CONCAT(v_nome,CONCAT(" ",v_apelido)), v_data_nascimento, 'birthParish', 'birthMunicipality', 'birthDistrict', 'birthCountry');
	
    -- Preencher Employee
    INSERT INTO easyid.general_employee (`user_id`)
    VALUES (LAST_INSERT_ID());
    
    COMMIT;
 
	END LOOP get_useremployee;
 
	CLOSE cursor_useremployee;
 
END //
 
DELIMITER ;

-- Course (Curso)
INSERT INTO easyid.general_course(`id`, `designation`, `teachingResearchUnits`)
SELECT c.idCurso, c.nome, (SELECT d.nome FROM fu.departamento as d WHERE d.idDepartamento = c.idDepartamento)
FROM fu.curso as c;

-- User e Student (Aluno)
CALL UserStudent();

-- User e Employee (Funcionario)
CALL UserEmployee();

-- User (Professor)
INSERT INTO easyid.general_user(`password`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `fullName`, `birthDate`, `birthParish`, `birthMunicipality`, `birthDistrict`, `birthCountry`)
SELECT 'password', 0, (idProfessor+(SELECT MAX(id) FROM easyid.general_user)), nome, apelido, email, 1, 0, '2020-01-01 20:00:00', CONCAT(nome,CONCAT(" ",apelido)), data_nascimento, 'birthParish', 'birthMunicipality', 'birthDistrict', 'birthCountry'
FROM fu.professor;