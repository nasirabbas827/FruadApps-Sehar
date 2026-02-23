-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 23, 2026 at 09:28 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fraudapps_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `applications`
--

CREATE TABLE `applications` (
  `app_id` int(11) NOT NULL,
  `application_name` varchar(150) NOT NULL,
  `link` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `rating` decimal(3,2) DEFAULT 0.00,
  `category` varchar(100) DEFAULT NULL,
  `app_image` varchar(255) DEFAULT NULL,
  `status` enum('genuine','fraud') NOT NULL DEFAULT 'genuine',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `applications`
--

INSERT INTO `applications` (`app_id`, `application_name`, `link`, `description`, `rating`, `category`, `app_image`, `status`, `created_at`) VALUES
(1, 'WhatsApp Messenger', 'https://whatsapp.com', 'Simple, reliable, and private messaging and calling.', 4.80, 'Communication', 'static/uploads/wp.jpg', 'fraud', '2026-02-23 07:48:08'),
(2, 'Instagram', 'https://instagram.com', 'A simple way to capture and share the worlds moments.', 4.50, 'Social', 'static/uploads/wp.jpg', 'fraud', '2026-02-23 07:48:08'),
(3, 'Notion', 'https://notion.so', 'The all-in-one workspace for your notes, tasks, and wikis.', 4.70, 'Productivity', 'static/uploads/wp.jpg', 'fraud', '2026-02-23 07:48:08'),
(4, 'Spotify', 'https://spotify.com', 'Digital music service that gives you access to millions of songs.', 4.60, 'Entertainment', 'static/uploads/wp.jpg', 'fraud', '2026-02-23 07:48:08'),
(5, 'Slack', 'https://slack.com', 'Slack is a new way to communicate with your team.', 4.40, 'Communication', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(6, 'Zoom Cloud Meetings', 'https://zoom.us', 'Stay connected wherever you go – start or join a secure meeting.', 4.20, 'Communication', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(7, 'Trello', 'https://trello.com', 'Trello’s boards, lists, and cards enable you to organize projects.', 4.30, 'Productivity', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(8, 'Discord', 'https://discord.com', 'Discord is the easiest way to talk over voice, video, and text.', 4.70, 'Social', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(9, 'Netflix', 'https://netflix.com', 'Watch TV shows and movies recommended just for you.', 4.50, 'Entertainment', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(10, 'LinkedIn', 'https://linkedin.com', 'Manage your professional identity. Build and engage with your network.', 4.10, 'Social', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(11, 'Candy Crush Saga', 'https://king.com', 'A sweet match 3 puzzle game that is easy to play.', 4.60, 'Games', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(12, 'PayPal', 'https://paypal.com', 'The simple and safe way to pay and get paid.', 4.40, 'Finance', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(13, 'Duolingo', 'https://duolingo.com', 'Learn a new language with the worlds most-downloaded education app.', 4.80, 'Education', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(14, 'Headspace', 'https://headspace.com', 'Guided meditation and mindfulness for everyday life.', 4.90, 'Health & Fitness', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(15, 'Pinterest', 'https://pinterest.com', 'Find recipes, style inspiration, and other ideas to try.', 4.60, 'Social', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(16, 'Microsoft Teams', 'https://microsoft.com', 'Chat, meet, call, and collaborate all in one place.', 4.00, 'Productivity', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(17, 'Adobe Lightroom', 'https://adobe.com', 'A powerful, free photo editor and camera app.', 4.70, 'Utilities', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(18, 'Uber', 'https://uber.com', 'Get a ride in minutes. Or deliver anything in your city.', 4.30, 'Utilities', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(19, 'Airbnb', 'https://airbnb.com', 'Unforgettable trips, experiences, and places to stay.', 4.70, 'Other', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(20, 'Telegram', 'https://telegram.org', 'Pure instant messaging. Simple, fast, secure, and synced.', 4.50, 'Communication', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(21, 'CapCut', 'https://capcut.com', 'An easy-to-use video editor for social media creators.', 4.80, 'Entertainment', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(22, 'Binance', 'https://binance.com', 'The worlds leading cryptocurrency exchange by volume.', 4.20, 'Finance', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(23, 'Asana', 'https://asana.com', 'Work anytime, anywhere with Asana. Stay on top of your tasks.', 4.30, 'Productivity', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(24, 'Coursera', 'https://coursera.org', 'Learn without limits. Start, switch, or advance your career.', 4.70, 'Education', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(25, 'MyFitnessPal', 'https://myfitnesspal.com', 'Track progress toward your nutrition, water, fitness, and weight goals.', 4.40, 'Health & Fitness', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(26, 'TikTok', 'https://tiktok.com', 'The leading destination for short-form mobile video.', 4.50, 'Entertainment', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(27, 'Reddit', 'https://reddit.com', 'The place where people come together to have the most authentic conversations.', 4.30, 'Social', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(28, 'Google Drive', 'https://google.com/drive', 'Store, share, and collaborate on files and folders.', 4.80, 'Productivity', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(29, 'Zomato', 'https://zomato.com', 'Discover great places to eat around you.', 4.10, 'Other', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08'),
(30, 'Twitter / X', 'https://twitter.com', 'Stay informed about what is happening in the world.', 3.90, 'Social', 'static/uploads/wp.jpg', 'genuine', '2026-02-23 07:48:08');

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `feedback_text` text NOT NULL,
  `status` enum('pending','read','resolved') NOT NULL DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`feedback_id`, `user_id`, `feedback_text`, `status`, `created_at`, `updated_at`) VALUES
(1, 1, 'This is Good', 'read', '2026-02-23 07:54:51', '2026-02-23 07:55:43');

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `review_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `app_id` int(11) NOT NULL,
  `review_text` text DEFAULT NULL,
  `sentiment_score` decimal(3,2) DEFAULT NULL,
  `ip_address` varchar(45) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `is_fake` tinyint(1) DEFAULT 0,
  `sentiment_label` varchar(20) NOT NULL DEFAULT 'Neutral'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`review_id`, `user_id`, `app_id`, `review_text`, `sentiment_score`, `ip_address`, `created_at`, `is_fake`, `sentiment_label`) VALUES
(1, 1, 30, 'I Hate this App', -0.21, '192.168.56.1', '2026-02-23 07:48:29', 0, 'Negative'),
(2, 1, 30, 'I Hate this App', -0.21, '192.168.56.1', '2026-02-23 07:48:35', 0, 'Negative'),
(3, 1, 30, 'I Hate this App', -0.21, '192.168.56.1', '2026-02-23 07:48:39', 0, 'Negative'),
(6, 1, 1, 'This is honestly one of the best messaging apps I’ve ever used. Super fast, reliable, and the privacy features actually work. 10/10 would recommend to everyone!', 0.26, '192.168.56.1', '2026-02-23 08:22:49', 0, 'Positive'),
(7, 1, 1, 'This is honestly one of the best messaging apps I’ve ever used. Super fast, reliable, and the privacy features actually work. 10/10 would recommend to everyone!', 0.26, '192.168.56.1', '2026-02-23 08:24:36', 0, 'Positive'),
(8, 1, 1, 'Way too many ads now. Every 2 minutes an ad pops up and it kills the experience. Used to be fun, now it\'s just frustrating.', 0.04, '192.168.56.1', '2026-02-23 08:25:50', 0, 'Neutral'),
(9, 1, 1, 'Way too many ads now. Every 2 minutes an ad pops up and it kills the experience. Used to be fun, now it\'s just frustrating. I Hate this App Boring App', 0.03, '192.168.56.1', '2026-02-23 08:26:28', 1, 'Neutral');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `profile_picture` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `first_name`, `last_name`, `profile_picture`) VALUES
(1, 'saifx280', 'saifx280@gmail.com', '123', 'Saif', 'Ullah', 'static/uploads/wp.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username_unique` (`username`);

--
-- Indexes for table `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`app_id`),
  ADD UNIQUE KEY `app_name_unique` (`application_name`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`feedback_id`),
  ADD KEY `fk_feedback_user` (`user_id`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`review_id`),
  ADD KEY `fk_reviews_user` (`user_id`),
  ADD KEY `fk_reviews_app` (`app_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username_unique` (`username`),
  ADD UNIQUE KEY `email_unique` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `applications`
--
ALTER TABLE `applications`
  MODIFY `app_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `feedback_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `review_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `feedback`
--
ALTER TABLE `feedback`
  ADD CONSTRAINT `feedback_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_app_fk` FOREIGN KEY (`app_id`) REFERENCES `applications` (`app_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `reviews_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
