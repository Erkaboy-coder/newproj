-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Фев 19 2022 г., 03:48
-- Версия сервера: 8.0.19
-- Версия PHP: 7.1.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `nurafshonnew`
--

-- --------------------------------------------------------

--
-- Структура таблицы `coaches`
--

CREATE TABLE `coaches` (
  `id` int UNSIGNED NOT NULL,
  `fio` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `position` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `lang_id` int NOT NULL,
  `age` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `coaches`
--

INSERT INTO `coaches` (`id`, `fio`, `position`, `region`, `image`, `lang_id`, `age`, `created_at`, `updated_at`) VALUES
(2, 'Нозимжон Эсанов', 'Ёрдамчи мураббий', 'Toshkent', 'images/7oVuNf12km17X4gZyUDwMWcja244DV56FYLkbIfm.jpeg', 1, '35', '2022-02-02 08:35:22', '2022-02-02 08:35:22');

-- --------------------------------------------------------

--
-- Структура таблицы `comments`
--

CREATE TABLE `comments` (
  `id` int UNSIGNED NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `lastname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `competitions`
--

CREATE TABLE `competitions` (
  `id` int UNSIGNED NOT NULL,
  `host_team_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `host_team_region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `host_team_logo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `against_team_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `against_team_logo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `against_team_region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `result` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `game_time` datetime NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `fotos`
--

CREATE TABLE `fotos` (
  `id` int UNSIGNED NOT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `image_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `image_slug` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `lang_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `fotos`
--

INSERT INTO `fotos` (`id`, `image`, `image_title`, `image_slug`, `lang_id`, `created_at`, `updated_at`) VALUES
(4, 'images/u92GtkBUFPaHQxr1q5FpSbrXFAKdH5keY5UoC13i.jpeg', 'Янги стадионда ўйин авжида', 'Янги стадионда ўйин авжида', 1, '2022-01-22 23:54:23', '2022-01-22 23:54:23'),
(5, 'images/2K8Ba9XYPfri0EdEYutGtwYZGEEI4LclEALWgafw.jpeg', 'Metallurg AKMK o\'yinidan lavhalar', 'Metallurg AKMK o\'yinada erishilgan ga\'laba hissiyotlari', 1, '2022-01-22 23:56:51', '2022-01-22 23:56:51'),
(6, 'images/I8xhQ7j5pvzUmmrDcTJOoPVz1Dv6bEFbC1Lc2wKE.jpeg', 'Foto lavhalar', 'Foto lavhalar', 1, '2022-01-22 23:58:20', '2022-01-22 23:58:20'),
(7, 'images/BTxpqOs8wpeV0G8iXEfQEn2hk3sSKawcsWSYn1kg.jpeg', 'Foto lavhalar', 'Foto lavhalar', 1, '2022-01-22 23:58:33', '2022-01-22 23:58:33'),
(8, 'images/KsxVKudAFcW434U7PxqmTvOtVZfvUJBwkP9x4wt8.jpeg', 'Foto lavhalar', 'Foto lavhalar', 1, '2022-02-02 10:03:30', '2022-02-02 10:03:30');

-- --------------------------------------------------------

--
-- Структура таблицы `games`
--

CREATE TABLE `games` (
  `id` int UNSIGNED NOT NULL,
  `team_home` int NOT NULL,
  `team_guest` int NOT NULL,
  `start_time` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `stadium_id` int NOT NULL DEFAULT '1',
  `league_id` int NOT NULL DEFAULT '1',
  `type_id` int NOT NULL,
  `is_finish` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `group_id` int NOT NULL,
  `is_next` tinyint(1) NOT NULL DEFAULT '0',
  `is_last` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `games`
--

INSERT INTO `games` (`id`, `team_home`, `team_guest`, `start_time`, `stadium_id`, `league_id`, `type_id`, `is_finish`, `created_at`, `updated_at`, `group_id`, `is_next`, `is_last`) VALUES
(7, 8, 9, '2022-01-23T09:31', 6, 1, 2, 1, '2022-01-22 23:29:31', '2022-01-22 23:33:38', 1, 0, 0),
(9, 8, 12, '2022-02-24T15:13', 6, 1, 8, 0, '2022-02-02 10:11:42', '2022-02-02 10:11:42', 1, 1, 0);

-- --------------------------------------------------------

--
-- Структура таблицы `goals`
--

CREATE TABLE `goals` (
  `id` int UNSIGNED NOT NULL,
  `goals_number` int NOT NULL,
  `time` int NOT NULL,
  `penalty` tinyint(1) NOT NULL DEFAULT '0',
  ` owngoal` tinyint(1) NOT NULL DEFAULT '0',
  `game_id` int NOT NULL DEFAULT '1',
  `team_id` int NOT NULL DEFAULT '1',
  `player_id` int NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `goals`
--

INSERT INTO `goals` (`id`, `goals_number`, `time`, `penalty`, ` owngoal`, `game_id`, `team_id`, `player_id`, `created_at`, `updated_at`) VALUES
(1, 1, 49, 0, 0, 1, 1, 7, '2018-12-12 04:56:13', '2018-12-12 04:56:13'),
(2, 1, 48, 0, 0, 2, 1, 6, '2018-12-12 05:48:41', '2018-12-12 05:48:41'),
(3, 1, 89, 0, 0, 1, 1, 8, '2018-12-12 12:31:47', '2018-12-12 12:31:47'),
(4, 1, 45, 0, 0, 3, 1, 3, '2018-12-12 13:15:15', '2018-12-12 13:15:15'),
(5, 1, 90, 0, 0, 1, 1, 5, '2018-12-19 13:52:50', '2018-12-19 13:52:50'),
(6, 1, 45, 0, 0, 5, 8, 3, '2022-01-22 22:56:39', '2022-01-22 22:56:39'),
(7, 1, 45, 0, 0, 7, 8, 2, '2022-01-22 23:33:38', '2022-01-22 23:33:38');

-- --------------------------------------------------------

--
-- Структура таблицы `groups`
--

CREATE TABLE `groups` (
  `id` int UNSIGNED NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `league_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `groups`
--

INSERT INTO `groups` (`id`, `name`, `league_id`, `created_at`, `updated_at`) VALUES
(1, 'A-GURUH', 1, NULL, NULL),
(2, 'B-GURUH', 1, NULL, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `langs`
--

CREATE TABLE `langs` (
  `id` int UNSIGNED NOT NULL,
  `lang_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `langs`
--

INSERT INTO `langs` (`id`, `lang_name`, `created_at`, `updated_at`) VALUES
(1, 'uz', NULL, NULL),
(2, 'ru', NULL, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `leadership_categories`
--

CREATE TABLE `leadership_categories` (
  `id` int UNSIGNED NOT NULL,
  `category_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `leadership_categories`
--

INSERT INTO `leadership_categories` (`id`, `category_name`, `created_at`, `updated_at`) VALUES
(1, 'Xodimlar', NULL, NULL),
(2, 'Akademiya xodimlari', NULL, NULL),
(3, 'Rahbariyat', NULL, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `leagues`
--

CREATE TABLE `leagues` (
  `id` int UNSIGNED NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `leagues`
--

INSERT INTO `leagues` (`id`, `name`, `created_at`, `updated_at`) VALUES
(1, 'Super liga', NULL, NULL),
(2, 'U-21', NULL, NULL),
(3, 'U-18', NULL, NULL),
(4, 'Ayollar', NULL, NULL),
(5, 'Futzal', NULL, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `mains`
--

CREATE TABLE `mains` (
  `id` int UNSIGNED NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `mains`
--

INSERT INTO `mains` (`id`, `name`, `created_at`, `updated_at`) VALUES
(1, 'Asosiy Tarkib', '2018-12-12 05:44:01', '2018-12-12 05:44:01'),
(4, 'U-21', NULL, NULL),
(5, 'U-18', NULL, NULL),
(7, 'Futzal\r\n', NULL, NULL),
(8, 'O\'yinchilar\r\n', NULL, NULL),
(9, 'Ayollar', NULL, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `matches`
--

CREATE TABLE `matches` (
  `id` int UNSIGNED NOT NULL,
  `game` int NOT NULL,
  `win` int NOT NULL,
  `lost` int NOT NULL,
  `equal` int NOT NULL,
  `goaldifference` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `score` int NOT NULL,
  `team_id` int NOT NULL,
  `league_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `matches`
--

INSERT INTO `matches` (`id`, `game`, `win`, `lost`, `equal`, `goaldifference`, `score`, `team_id`, `league_id`, `created_at`, `updated_at`) VALUES
(1, 21, 1, 1, 1, '1', 10, 8, 1, NULL, '2022-01-28 02:46:18'),
(2, 21, 2, 2, 2, '2', 9, 9, 1, NULL, '2022-01-28 02:46:18'),
(3, 21, 3, 3, 3, '3', 3, 10, 1, NULL, '2022-01-28 02:46:18'),
(4, 21, 4, 4, 4, '4', 4, 11, 1, NULL, '2022-01-28 02:46:18'),
(5, 21, 5, 5, 5, '5', 5, 12, 1, NULL, '2022-01-28 02:46:18'),
(6, 21, 6, 6, 6, '6', 6, 13, 1, NULL, '2022-01-28 02:46:18'),
(7, 21, 7, 7, 7, '7', 7, 14, 1, NULL, '2022-01-28 02:46:18'),
(8, 21, 8, 8, 8, '8', 8, 15, 1, NULL, '2022-01-28 02:46:18'),
(9, 21, 9, 9, 9, '9', 9, 16, 1, NULL, '2022-01-28 02:46:18'),
(10, 21, 10, 10, 10, '10', 10, 17, 1, NULL, '2022-01-28 02:46:18'),
(11, 21, 11, 11, 11, '11', 11, 18, 1, NULL, '2022-01-28 02:46:18'),
(12, 21, 12, 12, 12, '12', 12, 19, 1, NULL, '2022-01-28 02:46:18'),
(13, 21, 13, 13, 13, '13', 13, 20, 1, NULL, '2022-01-28 02:46:18'),
(14, 21, 14, 14, 14, '14', 14, 21, 1, NULL, '2022-01-28 02:46:18');

-- --------------------------------------------------------

--
-- Структура таблицы `migrations`
--

CREATE TABLE `migrations` (
  `id` int UNSIGNED NOT NULL,
  `migration` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `batch` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `migrations`
--

INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES
(1, '2014_10_12_000000_create_users_table', 1),
(2, '2014_10_12_100000_create_password_resets_table', 1),
(3, '2018_12_03_173740_create_news_table', 1),
(4, '2018_12_03_174445_create_teams_table', 1),
(5, '2018_12_03_174707_create_youngs_table', 1),
(6, '2018_12_03_174743_create_fotos_table', 1),
(7, '2018_12_03_174839_create_videos_table', 1),
(8, '2018_12_03_175533_create_competitions_table', 1),
(9, '2018_12_03_180949_create_leadership_categories_table', 1),
(10, '2018_12_03_181156_create_stadia_table', 1),
(11, '2018_12_03_181326_create_langs_table', 1),
(12, '2018_12_04_094249_create_comments_table', 1),
(13, '2018_12_05_085155_create_positions_table', 1),
(14, '2018_12_05_161314_create_players_table', 1),
(15, '2018_12_05_163121_create_leagues_table', 1),
(16, '2018_12_05_165534_create_goals_table', 1),
(17, '2018_12_05_172420_create_games_table', 1),
(18, '2018_12_06_145749_create_workers_table', 1),
(19, '2018_12_06_153850_create_types_table', 1),
(20, '2018_12_07_092518_create_mains_table', 1),
(21, '2018_12_08_132411_create_wins_table', 1),
(22, '2018_12_09_170918_create_coaches_table', 1),
(23, '2018_12_10_064920_create_groups_table', 1),
(24, '2018_12_10_065417_add_group_id_to_teams_table', 1),
(25, '2018_12_10_071145_add_group_id_to_games_table', 1),
(26, '2018_12_10_083348_add_next_game_to_games_table', 1),
(27, '2018_12_10_105727_add_goals_to_teams_table', 1),
(28, '2018_12_11_083725_add_is_last_to_games_table', 1),
(29, '2018_12_11_091630_create_stadions_table', 1),
(30, '2018_12_12_154533_create_youngs_table', 2),
(31, '2018_12_12_154651_create_women_table', 2),
(32, '2018_12_12_155235_add_weight_to_players_table', 2),
(33, '2018_12_12_155545_add_weight_to_players_table', 3),
(34, '2018_12_03_174445_create_matches_table', 4);

-- --------------------------------------------------------

--
-- Структура таблицы `news`
--

CREATE TABLE `news` (
  `id` int UNSIGNED NOT NULL,
  `news_slug` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `news_title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `news_body` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `lang_id` int NOT NULL,
  `news_image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `news`
--

INSERT INTO `news` (`id`, `news_slug`, `news_title`, `news_body`, `lang_id`, `news_image`, `created_at`, `updated_at`) VALUES
(2, '“Metallurg” – “Paxtakor” uchrashuvi rasmiylari', '“Metallurg” – “Paxtakor” uchrashuvi rasmiylari', '“Metallurg” – “Paxtakor” uchrashuvi rasmiylari 07.09.2020 Coca Cola Superliga 8-sentyabr kuni Coca Cola Superligasi 16-turidan o‘rin olgan “Metallurg” – “Paxtakor” o‘yini bo‘lib o‘tadi. Mazkur bellashuvni Rustam Lutfullin boshchiligidagi hakamlar brigadasi boshqarib boradi.', 1, 'images/QhGtjWVroOUY4vdWJVpN4mrQFdu8f5Y4zrWBeQvG.jpeg', '2022-01-23 00:02:52', '2022-01-23 00:02:52'),
(3, '“Bunyodkor” – “Metallurg” o‘yini Olmaliqda bo‘lib o‘tadi', '“Bunyodkor” – “Metallurg” o‘yini Olmaliqda bo‘lib o‘tadi', 'Davlat test imtihonlari “Bunyodkor” stadioniga tutash hududda ham o‘tkazilayotganidan kelib chiqib, abituriyentlarga halal bermaslik maqsadida Coca-Cola Superliga 15-turidan o‘rin olgan “Bunyodkor” — “Metallurg” uchrashuviga OKMK sport majmuasi mezbonlik qiladi.\r\n\r\nMazkur shaharda 15-avgust kuni AGMK klubi ham “Nasaf”ga qarshi uchrashuv o‘tkazishi, ketma-ket ikki kun davomidagi o‘yinlar maydon sifatiga ta’sir ko‘rsatishi mumkinlini inobatga olib, “Bunyodkor” — “Metallurg” uchrashuvi 14-avgust sanasida emas, balki 13-avgust kuni bo\'lib o\'tadi. Klublarning U-21 jamoalari ishtirokidagi bellashuv 12-avgust kuni “Bunyodkor” futbol akademiyasida tashkil etiladi.', 1, 'images/i5wg9IziU3sO0nVR4qKVA5Z2cDAHNTyDGR6d48ee.jpeg', '2022-01-23 00:05:33', '2022-01-23 00:05:33');

-- --------------------------------------------------------

--
-- Структура таблицы `password_resets`
--

CREATE TABLE `password_resets` (
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `players`
--

CREATE TABLE `players` (
  `id` int UNSIGNED NOT NULL,
  `fio` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `player_number` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `birthday` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `main_id` int NOT NULL DEFAULT '1',
  `region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `position_id` int NOT NULL,
  `team_id` int NOT NULL,
  `lang_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `weight` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '75 kg',
  `height` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '175 sm'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `players`
--

INSERT INTO `players` (`id`, `fio`, `image`, `player_number`, `birthday`, `main_id`, `region`, `position_id`, `team_id`, `lang_id`, `created_at`, `updated_at`, `weight`, `height`) VALUES
(2, 'Александр Лобанов', 'images/gnGOJTWloreQUkEnpR6JxkQOsZdwq0wJ7UXMC7Ye.jpeg', '12', '1989-08-19', 8, 'Toshkent Viloyati', 4, 8, 1, '2018-12-10 06:33:27', '2022-02-02 08:16:17', '75 kg', '175 sm'),
(3, 'Владимир Вагин', 'images/fDfgtY5CbWgn7wZA4iSbmwdp7CEXI22uUsZcXsTA.jpeg', '99', '1990-05-19', 8, 'Toshkent Viloyati', 4, 8, 1, '2018-12-10 06:34:15', '2022-02-02 08:16:02', '75 kg', '175 sm'),
(4, 'Саламат Қуттибоев', 'images/nSXikpWAfiVK5kULEcUtQ2MDqaOesoklGSSdRVtr.jpeg', '8', '1992-08-15', 8, 'Toshkent Viloyati', 2, 8, 1, '2018-12-10 06:34:54', '2022-02-02 08:16:53', '75 kg', '175 sm'),
(5, 'Аббос Отахонов', 'images/4CUo4CcXVICBTsgdivX8ZrrOd29ufbGM1SdxfXfh.jpeg', '5', '1990-12-12', 8, 'Toshkent Viloyati', 3, 8, 1, '2018-12-10 06:35:35', '2022-02-02 08:17:24', '75 kg', '175 sm'),
(6, 'Муҳаммад Исаев', 'images/Sd3AVjeHTgUxSI3WChIXtX2KZMfB92OJBUfdlhxh.jpeg', '77', '1997-05-18', 8, 'Toshkent Shahar', 2, 8, 1, '2018-12-10 06:36:55', '2022-02-02 08:17:54', '75 kg', '175 sm'),
(7, 'Аброр Тошқўзиев', 'images/0iFkwb8iDYi8biKvKf5tZL6I1sr1HtmugR3tjg5Z.jpeg', '14', '1990-12-12', 8, 'Toshkent Viloyati', 3, 8, 1, '2018-12-10 06:37:47', '2022-02-02 08:18:22', '75 kg', '175 sm'),
(8, 'Шаҳзодбек Ғофурбеков', 'images/UiFusPPPkdNdNUYqdeEQP2y1BkbrVYrWbFF3GOTW.jpeg', '22', '1990-12-12', 8, 'Toshkent Viloyati', 2, 8, 1, '2018-12-10 06:38:55', '2022-02-02 08:18:45', '75 kg', '175 sm'),
(9, 'Худойшукур Сатторов', 'images/G7pPlwtYrav14Qg5R6CqRUlcwQHyYpggdweKJbWj.jpeg', '20', '1990-12-12', 8, 'Toshkent Viloyati', 2, 8, 1, '2018-12-10 06:39:26', '2022-02-02 08:19:14', '75 kg', '175 sm'),
(10, 'Одилбек Абдумажидов', 'images/wEXucgp8tmanKWqrpj7H1KGubMupd9bTnGJqYVjy.jpeg', '4', '1990-08-19', 8, 'Toshkent Viloyati', 3, 8, 1, '2018-12-10 06:40:07', '2022-02-02 08:19:40', '75 kg', '175 sm'),
(11, 'Зоҳид Абдуллаев', 'images/i7fMxuaDczB5IMrBfZ5nLaQGBapuHsfxzrukeLjL.jpeg', '15', '1995-12-12', 8, 'Toshkent Viloyati', 1, 8, 1, '2018-12-10 06:41:43', '2022-02-02 08:20:02', '75 kg', '175 sm'),
(12, 'Ихтиёр Тошпўлатов', 'images/exac3F7BUNPJU1DaBv2vUyAxYi2OsxFIqWfZmsz4.jpeg', '27', '2021-12-30', 8, 'Xorazm', 2, 8, 1, '2022-01-23 04:24:38', '2022-02-02 08:20:35', '75', '170'),
(13, 'Aliya', 'images/5Mez13lNkYrhFMjHkQ2lS4tFPcQItl1F7LiPYYMW.jpeg', '98', '2022-01-05', 9, 'Xorazm', 1, 8, 1, '2022-01-23 05:41:46', '2022-01-23 05:41:46', '75', '170');

-- --------------------------------------------------------

--
-- Структура таблицы `positions`
--

CREATE TABLE `positions` (
  `id` int UNSIGNED NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `positions`
--

INSERT INTO `positions` (`id`, `name`, `created_at`, `updated_at`) VALUES
(1, 'Hujumchi', '2018-12-12 05:43:30', '2018-12-12 05:43:30'),
(2, 'Yarim Himoyachi', '2018-12-12 05:43:30', '2018-12-12 05:43:30'),
(3, 'Himoyachi', '2018-12-12 05:43:30', '2018-12-12 05:43:30'),
(4, 'Darvozabon', '2018-12-12 05:43:30', '2018-12-12 05:43:30');

-- --------------------------------------------------------

--
-- Структура таблицы `stadia`
--

CREATE TABLE `stadia` (
  `id` int UNSIGNED NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `about` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `stadia`
--

INSERT INTO `stadia` (`id`, `name`, `image`, `about`, `created_at`, `updated_at`) VALUES
(1, 'Nurafshon Stadioni', 'image', 'about', '2018-12-12 04:46:13', '2018-12-12 04:46:13'),
(2, 'Sherdor Stadioni', 'image', 'about', '2018-12-12 04:47:21', '2018-12-12 04:47:21'),
(3, 'Buhoro Stadioni', 'image', 'about', '2018-12-12 04:48:08', '2018-12-12 04:48:08'),
(4, 'Zomin Stadioni', 'image', 'about', '2018-12-12 04:48:53', '2018-12-12 04:48:53');

-- --------------------------------------------------------

--
-- Структура таблицы `stadions`
--

CREATE TABLE `stadions` (
  `id` int UNSIGNED NOT NULL,
  `stadion_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `stadion_slug` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `stadion_body` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `lang_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `stadions`
--

INSERT INTO `stadions` (`id`, `stadion_title`, `stadion_slug`, `stadion_body`, `image`, `lang_id`, `created_at`, `updated_at`) VALUES
(6, 'Metallurg', 'Metallurg stadioni', 'Metallurg stadioni', 'images/e30KqYvdSPLzeBC5dBVsB58R9EI9p2Uc98niwJ9w.jpeg', 1, '2022-01-22 22:44:27', '2022-01-23 00:29:51'),
(7, 'Paxtokor', 'Paxtakor stadioni', 'Paxtakor stadioni', 'images/fHiHJ6y6veezJG6BOWOoSvf5WKQojqn39oqPwd0D.jpeg', 1, '2022-01-22 22:50:15', '2022-01-23 00:30:41'),
(8, 'Bunyodkor', 'Bunyodkor stadioni', 'Bunyodkor stadioni', 'images/eKTToRT1IAKwUQqUeIjzRIOnzUKGjlfD7wwevTvZ.jpeg', 1, '2022-01-22 22:50:32', '2022-01-23 00:30:51'),
(9, 'АГМК', 'АГМК', 'АГМК', 'images/8hx74GZIHU4ehGAx2Vq4suXazLVqt8tKDQVFZTam.jpeg', 1, '2022-01-27 07:45:47', '2022-01-27 07:45:47'),
(10, 'Насаф', 'Насаф', 'Насаф', 'images/YNjijS0XuD7jkcUbnqYDyJBeVexFUCgF7j8NKCcM.jpeg', 1, '2022-01-27 07:50:20', '2022-01-27 07:50:20'),
(11, 'Сўғдиёна', 'Сўғдиёна', 'Сўғдиёна', 'images/MbDY2xmr6PBwiYDRCFrCet4fP04TKdiQ71e6ReBy.jpeg', 1, '2022-01-27 07:50:37', '2022-01-27 07:50:37'),
(12, 'Локомотив', 'Локомотив', 'Локомотив', 'images/Tq2LOTmQyTU8JlpZ0Xy3Ivq1TdPpClgnLJmsDYvk.jpeg', 1, '2022-01-27 07:50:50', '2022-01-27 07:50:50'),
(13, 'Навбаҳор', 'Навбаҳор', 'Навбаҳор', 'images/euahS72l4uKpglt7lYaFsp9SXKQOpMsAVnK9aI7m.jpeg', 1, '2022-01-27 07:52:11', '2022-01-27 07:52:11'),
(14, 'Қўқон-1912', 'Қўқон-1912', 'Қўқон-1912', 'images/Qn2Y9PeoVjGBb7PTVFI5mp0NhBAacDltYfVkGFWz.jpeg', 1, '2022-01-27 07:52:21', '2022-01-27 08:00:32'),
(15, 'Машъал', 'Машъал', 'Машъал', 'images/pj760A53EQGJEOq1BbeBnwwWeuM4LYC3u8ihSAuK.jpeg', 1, '2022-01-27 07:52:33', '2022-01-27 08:00:56'),
(16, 'Қизилқум', 'Қизилқум', 'Қизилқум', 'images/eYN1pWMGs9dpwYL1jpafkAiN9ndcHcTuRrkocfy2.jpeg', 1, '2022-01-27 07:52:45', '2022-01-27 07:59:54'),
(17, 'Андижон', 'Андижон', 'Андижон', 'images/GQ5jsMajQayAaKzLEa2YvXhpiL08cjeXBj7jFnUM.jpeg', 1, '2022-01-27 07:53:18', '2022-01-27 07:53:18'),
(18, 'Сурхон', 'Сурхон', 'Сурхон', 'images/XKMGHcWCuG0nC9tUAoPRy6yLOjjGzNMevStdmHFj.jpeg', 1, '2022-01-27 07:53:32', '2022-01-27 07:53:32'),
(19, 'Турон', 'Турон', 'Турон', 'images/Ri3YpLV7jVC0AC35Td0onh8xERLHUKlZFwS8SSlk.jpeg', 1, '2022-01-27 07:53:53', '2022-01-27 07:53:53');

-- --------------------------------------------------------

--
-- Структура таблицы `teams`
--

CREATE TABLE `teams` (
  `id` int UNSIGNED NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `year` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `score` int NOT NULL DEFAULT '0',
  `number_wins` int NOT NULL DEFAULT '0',
  `stadium_id` int NOT NULL,
  `league_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `group_id` int NOT NULL,
  `goals_number` int NOT NULL DEFAULT '0',
  `goals_reverse` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `teams`
--

INSERT INTO `teams` (`id`, `name`, `image`, `year`, `region`, `score`, `number_wins`, `stadium_id`, `league_id`, `created_at`, `updated_at`, `group_id`, `goals_number`, `goals_reverse`) VALUES
(8, 'Metallurg', 'images/J631f6s2k0qh2WjjykFjpTiljFHotVVdvobg5K2x.png', '2018', 'Toshkent', 9, 0, 6, 1, '2022-01-22 22:44:53', '2022-02-02 10:12:33', 1, 2, 0),
(9, 'Paxtokor', 'images/tKQcR63OdXR3RVVYUcOK3RbY2292TrnM5LUSCfKN.png', '2018', 'Toshkent', 3, 0, 7, 1, '2022-01-22 22:51:02', '2022-01-22 23:33:38', 1, 0, 2),
(10, 'Bunyodkor', 'images/2JLwawJRW3j6KPatwRuoKcIIHiBRmBRQYMNgweET.png', '2018', 'Toshkent', 3, 0, 8, 1, '2022-01-22 22:51:19', '2022-02-02 10:12:33', 1, 0, 0),
(11, 'АГМК', 'images/DGaraqfoEZTTgPo0uK8ZSbZD3zyjbDtjoycVlwf7.png', '2018', 'Toshkent', 0, 0, 9, 1, '2022-01-27 07:56:37', '2022-01-27 07:56:37', 1, 0, 0),
(12, 'Насаф', 'images/BVNcN4Z5gwEZD2sGaewrxaXQbsJBBixfrNIoC4TG.png', '2018', 'Qashqadaryo', 0, 0, 10, 1, '2022-01-27 07:57:04', '2022-01-27 07:57:04', 1, 0, 0),
(13, 'Сўғдиёна', 'images/eDaofilYakbGfjzoqSiAzFgktiwqjHuedUyQu3j4.png', '2018', 'Сўғдиёна', 0, 0, 11, 1, '2022-01-27 07:57:53', '2022-01-27 07:57:53', 1, 0, 0),
(14, 'Локомотив', 'images/je6h2sB3QlEqohsvQZoAHTZHDhrkdz54eFFMkb1L.png', '2018', 'Toshkent', 0, 0, 12, 1, '2022-01-27 07:58:15', '2022-01-27 07:58:15', 1, 0, 0),
(15, 'Навбаҳор', 'images/XCZxsrsttU07MhJe06hidyqYMmTYDVQEqvqgce0R.png', '2018', 'Namangan', 0, 0, 14, 1, '2022-01-27 07:58:54', '2022-01-27 07:58:54', 1, 0, 0),
(16, 'Қизилқум', 'images/okU5Wltczv4GdI7Axukvdd4dEEi9n56XAi8htRRY.png', '2018', 'Қизилқум', 0, 0, 16, 1, '2022-01-27 08:02:07', '2022-01-27 08:02:07', 1, 0, 0),
(17, 'Қўқон-1912', 'images/QT7AetQwE3LYTNT6SB498HhlsurcYupmeZAV2cV0.png', '1912', 'Қўқон', 0, 0, 14, 1, '2022-01-27 08:02:33', '2022-02-07 06:06:57', 1, 0, 0),
(18, 'Машъал', 'images/ePezP90FrvzLqwdkhtg0EnfcxWAPC4bu7dGPrmhF.png', '2018', 'Машъал', 0, 0, 15, 1, '2022-01-27 08:02:52', '2022-01-27 08:02:52', 1, 0, 0),
(19, 'Андижон', 'images/HHGVihcAZdEFNeyAbty4nCNo4uTPiZYCZbi7kdCN.png', '2018', 'Андижон', 0, 0, 17, 1, '2022-01-27 08:04:10', '2022-01-27 08:04:10', 1, 0, 0),
(20, 'Сурхон', 'images/5Y7MqW1w57Q94MTVG0xcq5OsBvGc06fm4NTbdVZi.png', '2018', 'Surxandaryo', 0, 0, 18, 1, '2022-01-27 08:04:39', '2022-01-27 08:04:39', 1, 0, 0),
(21, 'Турон', 'images/oxjbM064xZqztXmfGlEENJDSfqYvV9wDXvSgHejs.png', '2018', 'Турон', 0, 0, 19, 1, '2022-01-27 08:05:05', '2022-01-27 08:05:05', 1, 0, 0);

-- --------------------------------------------------------

--
-- Структура таблицы `types`
--

CREATE TABLE `types` (
  `id` int UNSIGNED NOT NULL,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `types`
--

INSERT INTO `types` (`id`, `name`, `created_at`, `updated_at`) VALUES
(1, '1-tur', '2018-12-12 04:52:37', '2018-12-12 04:52:37'),
(2, '2-tur', '2018-12-12 04:52:37', '2018-12-12 04:52:37'),
(3, '3-tur', '2018-12-12 04:52:37', '2018-12-12 04:52:37'),
(4, '4-tur', '2018-12-12 04:52:37', '2018-12-12 04:52:37'),
(5, '5-tur', '2018-12-12 04:52:37', '2018-12-12 04:52:37'),
(6, '6-tur', '2018-12-12 04:52:37', '2018-12-12 04:52:37'),
(7, '7-tur', '2018-12-12 04:52:37', '2018-12-12 04:52:37'),
(8, '8-tur', '2018-12-12 04:52:37', '2018-12-12 04:52:37'),
(9, '9-tur', '2018-12-12 04:52:37', '2018-12-12 04:52:37'),
(10, '10-tur', '2018-12-12 04:52:37', '2018-12-12 04:52:37'),
(11, '11', NULL, NULL),
(12, '12', NULL, NULL),
(13, '13', NULL, NULL),
(14, '14', NULL, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int UNSIGNED NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `remember_token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `email_verified_at`, `password`, `remember_token`, `created_at`, `updated_at`) VALUES
(2, 'Jahongir', 'jumaniyozov@gmail.com', NULL, '$2y$10$61dDLScaHaFNWPOmfRM1DeUoam3V909HjehC.Xr87RCnwXN2x6eq6', NULL, '2018-12-12 11:04:06', '2018-12-12 11:04:06'),
(3, 'Admin', 'admin@mail.com', NULL, '$2y$10$OzMR7iTwSFBIi6TggoMKPus5qnCISYKg1i4TguxtpLSD8EooWe2QC', NULL, '2018-12-13 03:06:17', '2018-12-13 03:06:17'),
(7, 'User', 'user@gmail.com', NULL, '$2y$10$xzUb01iqIsgfn0gc/2d4FezUREQeukWWghLKqMHAHbTSNOckQOd1y', NULL, '2022-01-18 08:44:03', '2022-01-18 08:44:03'),
(8, 'admin2', 'admin2@gmail.com', NULL, '$2y$10$9PFMVvbVHq7q3DyMNROtku0u0zWxlrGg9tz8Qh8EOUSKzEwLqy4mu', 'Oa5Di883PDm57U3KxBT4PsSVEH81Zas2k2P1WNXJjbFbFMC6rtbk8SAeGSd1', '2022-01-18 23:55:37', '2022-01-18 23:55:37');

-- --------------------------------------------------------

--
-- Структура таблицы `videos`
--

CREATE TABLE `videos` (
  `id` int UNSIGNED NOT NULL,
  `video_link` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `video_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `lang_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `videos`
--

INSERT INTO `videos` (`id`, `video_link`, `video_title`, `lang_id`, `created_at`, `updated_at`) VALUES
(1, 'https://www.youtube.com/embed/nSblgPqKtwo', 'Gollar', 1, '2022-01-18 08:52:42', '2022-01-18 08:52:42');

-- --------------------------------------------------------

--
-- Структура таблицы `wins`
--

CREATE TABLE `wins` (
  `id` int UNSIGNED NOT NULL,
  `wins_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `wins_body` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `lang_id` int NOT NULL,
  `wins_image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `wins`
--

INSERT INTO `wins` (`id`, `wins_title`, `wins_body`, `lang_id`, `wins_image`, `created_at`, `updated_at`) VALUES
(2, 'Surxon ustidan g\'alaba', 'Kecha o\'tkazilgan Surxon Metallurk o\'yinida Metallurk jamoasi 0:4 xisobda g\'alaba qozondi', 1, 'images/uJqQJFKfk3osxw5P32acNfZQxrzyiAzDe7n0F6FN.jpeg', '2022-01-22 20:50:59', '2022-01-22 20:50:59');

-- --------------------------------------------------------

--
-- Структура таблицы `women`
--

CREATE TABLE `women` (
  `id` int UNSIGNED NOT NULL,
  `fio` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `player_number` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `birthday` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `main_id` int NOT NULL DEFAULT '1',
  `region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `position_id` int NOT NULL,
  `weight` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '60 kg',
  `height` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '160 sm',
  `team_id` int NOT NULL DEFAULT '1',
  `lang_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `women`
--

INSERT INTO `women` (`id`, `fio`, `image`, `player_number`, `birthday`, `main_id`, `region`, `position_id`, `weight`, `height`, `team_id`, `lang_id`, `created_at`, `updated_at`) VALUES
(1, 'Aziza Aliyeva', 'images/FmnqGnN6DyTVJsLh1Y6eEGs1JFKvunBX5M03Zea3.jpeg', '45', '1990-12-19', 1, 'Toshkent Viloyati', 1, '60 kg', '160 sm', 8, 2, '2018-12-12 11:21:43', '2018-12-15 13:14:20');

-- --------------------------------------------------------

--
-- Структура таблицы `workers`
--

CREATE TABLE `workers` (
  `id` int UNSIGNED NOT NULL,
  `fio` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `position` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `category_id` int NOT NULL,
  `lang_id` int NOT NULL,
  `tel_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `workers`
--

INSERT INTO `workers` (`id`, `fio`, `position`, `image`, `category_id`, `lang_id`, `tel_number`, `created_at`, `updated_at`) VALUES
(2, 'Комилжон Жумаев', 'матбуот котиби', 'images/2rAETsqpnPK2SdFlm6dEZ5RhTgLffsJFV4cDSrIM.jpeg', 1, 1, '---------', '2022-02-02 08:29:54', '2022-02-02 08:29:54'),
(3, 'Акмал Содиқов', 'Бошҳисобчи', 'images/OkRMOZCFhZDHYh0dj6arKVBGWoWFW3wbNAjbgYSj.jpeg', 1, 1, '+99 89* *** ** **', '2022-02-02 08:32:12', '2022-02-02 08:32:12'),
(4, 'Аллишер Тошматов', 'Хавфсизлик ишлари бўйича офицер', 'images/x3FnEjJKTkjhVIJVCVom8FLdpjMKKG2WMlK9PLrS.jpeg', 1, 1, '+ 99 89* *** ** **', '2022-02-02 08:32:53', '2022-02-02 08:32:53'),
(5, 'Сорокина Валентина Махмудовна', 'Ёрдамчи ҳисобчи', 'images/73cMUIcheho6tjndPpCPlJKOpSwqYVaEivwpzqLB.jpeg', 1, 1, '+99 89* *** ** **', '2022-02-02 08:33:58', '2022-02-02 08:33:58'),
(6, 'Шохида Нурматова', 'Xуқуқшунос', 'images/fEW4fV2RoiuDxTTY0kDCuu22ZwQmwUyHrwIbmajS.jpeg', 1, 1, '+99 89* *** ** **', '2022-02-02 08:34:26', '2022-02-02 08:34:26'),
(7, 'Қаҳрамон Нурматов', '\"Металлург-W\" жамоаси бошлиғи', 'images/TftB9TD2XORfNH6zVogYwfIMIt3X6wp8mkhbTDcR.jpeg', 3, 1, '+99 89* *** ** **', '2022-02-02 10:00:15', '2022-02-02 10:00:15');

-- --------------------------------------------------------

--
-- Структура таблицы `youngs`
--

CREATE TABLE `youngs` (
  `id` int UNSIGNED NOT NULL,
  `fio` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `player_number` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `birthday` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `main_id` int NOT NULL DEFAULT '1',
  `region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `position_id` int NOT NULL,
  `team_id` int NOT NULL,
  `weight` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '65 kg',
  `height` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '165 sm',
  `lang_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `youngs`
--

INSERT INTO `youngs` (`id`, `fio`, `image`, `player_number`, `birthday`, `main_id`, `region`, `position_id`, `team_id`, `weight`, `height`, `lang_id`, `created_at`, `updated_at`) VALUES
(1, 'Diyorbek', 'images/KlhnnDOGxaSCzJ4BsybJ7xefUj7BbqXJYMgUQhgt.jpeg', '7', '2003-02-08', 1, 'Xorazm', 1, 1, '66kg', '169sm', 2, '2018-12-15 03:49:17', '2018-12-15 12:56:14');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `coaches`
--
ALTER TABLE `coaches`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `competitions`
--
ALTER TABLE `competitions`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `fotos`
--
ALTER TABLE `fotos`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `games`
--
ALTER TABLE `games`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `goals`
--
ALTER TABLE `goals`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `groups`
--
ALTER TABLE `groups`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `langs`
--
ALTER TABLE `langs`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `leadership_categories`
--
ALTER TABLE `leadership_categories`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `leagues`
--
ALTER TABLE `leagues`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `mains`
--
ALTER TABLE `mains`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `matches`
--
ALTER TABLE `matches`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `migrations`
--
ALTER TABLE `migrations`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `news`
--
ALTER TABLE `news`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `password_resets`
--
ALTER TABLE `password_resets`
  ADD KEY `password_resets_email_index` (`email`);

--
-- Индексы таблицы `players`
--
ALTER TABLE `players`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `positions`
--
ALTER TABLE `positions`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `stadia`
--
ALTER TABLE `stadia`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `stadions`
--
ALTER TABLE `stadions`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `teams`
--
ALTER TABLE `teams`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `types`
--
ALTER TABLE `types`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `types_name_unique` (`name`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_email_unique` (`email`);

--
-- Индексы таблицы `videos`
--
ALTER TABLE `videos`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `wins`
--
ALTER TABLE `wins`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `women`
--
ALTER TABLE `women`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `workers`
--
ALTER TABLE `workers`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `youngs`
--
ALTER TABLE `youngs`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `coaches`
--
ALTER TABLE `coaches`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `comments`
--
ALTER TABLE `comments`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `competitions`
--
ALTER TABLE `competitions`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `fotos`
--
ALTER TABLE `fotos`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `games`
--
ALTER TABLE `games`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT для таблицы `goals`
--
ALTER TABLE `goals`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT для таблицы `groups`
--
ALTER TABLE `groups`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `langs`
--
ALTER TABLE `langs`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `leadership_categories`
--
ALTER TABLE `leadership_categories`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `leagues`
--
ALTER TABLE `leagues`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `mains`
--
ALTER TABLE `mains`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT для таблицы `matches`
--
ALTER TABLE `matches`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT для таблицы `migrations`
--
ALTER TABLE `migrations`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT для таблицы `news`
--
ALTER TABLE `news`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `players`
--
ALTER TABLE `players`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT для таблицы `positions`
--
ALTER TABLE `positions`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `stadia`
--
ALTER TABLE `stadia`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `stadions`
--
ALTER TABLE `stadions`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT для таблицы `teams`
--
ALTER TABLE `teams`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT для таблицы `types`
--
ALTER TABLE `types`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `videos`
--
ALTER TABLE `videos`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `wins`
--
ALTER TABLE `wins`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `women`
--
ALTER TABLE `women`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `workers`
--
ALTER TABLE `workers`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT для таблицы `youngs`
--
ALTER TABLE `youngs`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
