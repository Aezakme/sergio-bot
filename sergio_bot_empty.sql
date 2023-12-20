/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for sergiobot
CREATE DATABASE IF NOT EXISTS `sergiobot` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `sergiobot`;

-- Dumping structure for table sergiobot.chat_users
CREATE TABLE IF NOT EXISTS `chat_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` bigint(20) DEFAULT NULL,
  `cid` bigint(20) DEFAULT NULL,
  `left` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=218;

-- Data exporting was unselected.

-- Dumping structure for table sergiobot.leave_logs
CREATE TABLE IF NOT EXISTS `leave_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` bigint(20) DEFAULT NULL,
  `cid` bigint(20) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `leave_type` enum('added','invite','kicked','left') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `from_uid` bigint(20) DEFAULT NULL,
  `reason` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AVG_ROW_LENGTH=81;

-- Data exporting was unselected.

-- Dumping structure for table sergiobot.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` bigint(20) DEFAULT NULL,
  `username` text COLLATE utf8mb4_unicode_ci,
  `fullname` text COLLATE utf8mb4_unicode_ci,
  `public` tinyint(1) DEFAULT NULL,
  `female` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AVG_ROW_LENGTH=54;

-- Data exporting was unselected.

-- Dumping structure for table sergiobot.user_stats
CREATE TABLE IF NOT EXISTS `user_stats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stats_monday` datetime DEFAULT NULL,
  `uid` bigint(20) DEFAULT NULL,
  `cid` bigint(20) DEFAULT NULL,
  `last_activity` datetime DEFAULT NULL,
  `all_messages_count` int(11) DEFAULT NULL,
  `sent_replies_count` int(11) DEFAULT NULL,
  `received_replies_count` int(11) DEFAULT NULL,
  `forwards_count` int(11) DEFAULT NULL,
  `text_messages_count` int(11) DEFAULT NULL,
  `text_messages_with_obscene_count` int(11) DEFAULT '0',
  `audios_count` int(11) DEFAULT NULL,
  `documents_count` int(11) DEFAULT NULL,
  `gifs_count` int(11) DEFAULT NULL,
  `photos_count` int(11) DEFAULT NULL,
  `stickers_count` int(11) DEFAULT NULL,
  `videos_count` int(11) DEFAULT NULL,
  `video_notes_count` int(11) DEFAULT NULL,
  `video_notes_duration` int(11) DEFAULT NULL,
  `voices_count` int(11) DEFAULT NULL,
  `voices_duration` int(11) DEFAULT NULL,
  `games_count` int(11) DEFAULT NULL,
  `sent_mentions_count` int(11) DEFAULT NULL,
  `received_mentions_count` int(11) DEFAULT NULL,
  `hashtags_count` int(11) DEFAULT NULL,
  `bot_commands_count` int(11) DEFAULT NULL,
  `urls_count` int(11) DEFAULT NULL,
  `emails_count` int(11) DEFAULT NULL,
  `words_count` int(11) DEFAULT NULL,
  `obscene_words_count` int(11) DEFAULT '0',
  `chars_count` int(11) DEFAULT NULL,
  `chars_wo_space_count` int(11) DEFAULT NULL,
  `emoji_count` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `top_domain` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AVG_ROW_LENGTH=478;

-- Data exporting was unselected.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;