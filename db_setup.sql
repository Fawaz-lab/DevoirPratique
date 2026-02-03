-- Script de configuration de la base de données
-- À exécuter dans votre client MySQL (Workbench, PHPMyAdmin, ou ligne de commande) en tant que root

-- 1. Création de la base de données
CREATE DATABASE IF NOT EXISTS family_expenses;

-- 2. Création de l'utilisateur dédié 'famille_user'
-- Note: Si l'utilisateur existe déjà, cette commande ne fera rien (sur MySQL récent)
-- ou vous pouvez ignorer l'erreur si elle survient.
CREATE USER IF NOT EXISTS 'famille_user'@'localhost' IDENTIFIED BY 'FAWAZ1*3*5*7*';

-- 3. Attribution des droits
GRANT ALL PRIVILEGES ON family_expenses.* TO 'famille_user'@'localhost';

-- 4. Prise en compte des changements
FLUSH PRIVILEGES;
