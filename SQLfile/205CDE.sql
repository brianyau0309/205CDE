-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 09, 2019 at 10:29 PM
-- Server version: 5.7.25-0ubuntu0.18.04.2
-- PHP Version: 7.2.15-0ubuntu0.18.04.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `205CDE`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `adminID` int(11) NOT NULL,
  `account` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `client` enum('N','R','RW') NOT NULL DEFAULT 'RW',
  `article` enum('N','R','RW') NOT NULL DEFAULT 'RW',
  `news` enum('N','R','RW') NOT NULL DEFAULT 'RW',
  `carousel` enum('N','R','RW') NOT NULL DEFAULT 'RW',
  `comment` enum('N','R','RW') NOT NULL DEFAULT 'RW',
  `revenue` enum('N','R') NOT NULL DEFAULT 'R',
  `admin` enum('Normal','Super') NOT NULL DEFAULT 'Normal',
  `record` enum('N','R') NOT NULL DEFAULT 'R'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`adminID`, `account`, `password`, `client`, `article`, `news`, `carousel`, `comment`, `revenue`, `admin`, `record`) VALUES
(1, 'admin1', 'admin1', 'RW', 'RW', 'RW', 'RW', 'RW', 'R', 'Super', 'R'),
(2, 'admin2', 'admin2', 'N', 'R', 'R', 'R', 'R', 'R', 'Normal', 'R'),
(3, 'admin3', 'admin3', 'R', 'R', 'RW', 'R', 'R', 'R', 'Normal', 'R'),
(4, 'admin4', 'admin4', 'R', 'N', 'RW', 'N', 'N', 'R', 'Normal', 'R'),
(5, 'admin5', 'admin5', 'R', 'R', 'R', 'R', 'R', 'R', 'Normal', 'R');

-- --------------------------------------------------------

--
-- Table structure for table `article`
--

CREATE TABLE `article` (
  `articleID` int(11) NOT NULL,
  `title` varchar(99) NOT NULL,
  `price` double(9,2) NOT NULL,
  `description` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `date` datetime NOT NULL,
  `owner` int(11) NOT NULL,
  `sales` int(11) NOT NULL DEFAULT '0',
  `category` varchar(20) NOT NULL,
  `state` enum('able','disable') NOT NULL DEFAULT 'able'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `article`
--

INSERT INTO `article` (`articleID`, `title`, `price`, `description`, `content`, `date`, `owner`, `sales`, `category`, `state`) VALUES
(1, 'Here is Title', 10.00, 'Here is description', 'Example Content:\r\n1. Preheat oven to 350 degrees F (175 degrees C). Spray 12 muffin cups with cooking spray.\r\n2. Cook and stir bacon in a skillet over medium-high heat until crisp, about 10 minutes. Transfer bacon to a bowl, reserving bacon grease in the skillet.\r\n3. Combine spinach, mushrooms, green bell pepper, onion, salt, and ground black pepper to taste in the skillet with bacon grease; cook and stir until softened, about 5 minutes. Transfer vegetable mixture to a bowl and place in the freezer to cool, about 5 minutes.\r\n4. Whisk eggs and cream together in a bowl; stir in 1 cup Colby-Jack cheese, 1/2 teaspoon salt, 1/4 teaspoon ground black pepper, onion powder, and garlic powder. Add cooled vegetables and bacon to egg mixture and mix gently.\r\n5. Scoop 1/4 cup egg mixture into each muffin cup; top each with remaining Colby-Jack cheese.\r\n6. Bake in the preheated oven until egg cups are set, about 20 minutes.', '2019-03-27 17:56:05', 1, 6, 'chinese', 'able'),
(2, 'Example Article 1', 20.00, 'Example Article 1 Description', '1. Preheat oven to 425 degrees F (220 degrees C). Lightly oil a large roasting pan.\r\n2. Place chicken pieces in large bowl. Season with salt, oregano, pepper, rosemary, and cayenne pepper. Add fresh lemon juice, olive oil, and garlic. Place potatoes in bowl with the chicken; stir together until chicken and potatoes are evenly coated with marinade.\r\n3. Transfer chicken pieces, skin side up, to prepared roasting pan, reserving marinade. Distribute potato pieces among chicken thighs. Drizzle with 2/3 cup chicken broth. Spoon remainder of marinade over chicken and potatoes.\r\n4. Place in preheated oven. Bake in the preheated oven for 20 minutes. Toss chicken and potatoes, keeping chicken skin side up; continue baking until chicken is browned and cooked through, about 25 minutes more. An instant-read thermometer inserted near the bone should read 165 degrees F (74 degrees C). Transfer chicken to serving platter and keep warm.\r\n5.  Set oven to broil or highest heat setting. Toss potatoes once again in pan juices. Place pan under broiler and broil until potatoes are caramelized, about 3 minutes. Transfer potatoes to serving platter with chicken.\r\n6. Place roasting pan on stove over medium heat. Add a splash of broth and stir up browned bits from the bottom of the pan. Strain; spoon juices over chicken and potatoes. Top with chopped oregano.\r\n', '2019-03-27 19:20:39', 1, 1, 'other', 'able'),
(3, 'Example Article 2', 20.00, 'Example Article 2 Description', 'Step 1. Adjust an oven rack to the top position and preheat oven to 425 degrees. Wash and dry all produce. Peel and grate or mince ginger.\r\n\r\nStep 2. In a small pot, combine rice, ¾ cup water, and a large pinch of salt. Bring to a boil. Once boiling, cover and reduce to low heat. Cook until water has absorbed and rice is tender, about 15 minutes. Turn off heat; keep covered until ready to serve.\r\n\r\nStep 3. Toss green beans on a baking sheet with a drizzle of oil, salt, and pepper. Roast until browned and tender, about 15 minutes.\r\n\r\nStep 4. Pat chicken dry with paper towels; season all over with salt and pepper. Heat a drizzle of oil in a large pan over medium-high heat. Add chicken and cook until browned and cooked through, 3-4 minutes per side. Turn off heat; transfer chicken to a plate.\r\n\r\nStep 5. Add half the ginger (or more if you like food a little spicy) to same pan. Cook on medium heat until fragrant, 30-60 seconds. Add jam, stock concentrate, and ¼ cup water. Stir to combine and cook until thickened, 1-2 minutes. Turn off heat; stir in 1 TBSP butter until melted.\r\n\r\nStep 6. Fluff rice with a fork. Stir in 1 TBSP butter until melted; season with salt and pepper. Divide rice, chicken, and green beans between plates. Top chicken with sauce.', '2019-03-27 21:06:48', 1, 1, 'japanese', 'able'),
(4, 'Example Article 3', 30.00, 'Example Article 3 Description', '1.\r\n2.\r\n3.\r\n4.\r\n5.\r\n6.\r\n7.\r\n8.\r\n9.\r\n10.\r\n11.\r\n12.\r\n13.\r\n14.\r\n15.', '2019-03-27 21:16:34', 3, 4, 'other', 'able'),
(5, 'Example Article 4', 40.00, 'Example Article 4 Description', '1. Just for example\r\n2.\r\n3.\r\n4.\r\n5.\r\n6.\r\n7.\r\n8.\r\n9.\r\n10.\r\n11.\r\n12.\r\n13.\r\n14.\r\n15.', '2019-03-27 21:17:17', 3, 1, 'other', 'able'),
(6, 'Example Article 5', 50.00, 'Example Article 5 Description', '1. Wash and dry all produce. Adjust rack to middle position and preheat oven to 450 degrees. Slice sweet potatoes into ¼-inch-thick rounds. Toss on a baking sheet with a drizzle of olive oil, 1 tsp harissa powder (we’ll use more later), and a pinch of salt and pepper. Roast in oven until tender, about 20 minutes, flipping halfway through.\r\n\r\n2. Mince or grate 1 clove garlic (we sent more). Halve cucumber lengthwise, then slice into thin half-moons. Pick and roughly chop enough fronds from dill to give you 2 tsp. Halve, pit, and peel avocado, then thinly slice.\r\n\r\n3. In a small bowl, combine 3 TBSP mayonnaise (we sent more), a pinch of garlic, and a pinch of harissa powder. Give mixture a taste and add more garlic and harissa powder as desired. Season with salt and pepper.\r\n\r\n4. In a medium bowl, toss cucumber, chopped dill, vinegar, a drizzle of olive oil, and a pinch of salt and pepper.\r\n\r\n5. Cut pitas in half to create 4 pockets and place on another baking sheet. When sweet potatoes are almost done, after 18-20 minutes of roasting, put pitas in oven. Toast until warmed through but not crispy, 2-3 minutes. TIP: If there’s room, you can place pitas on the same baking sheet as sweet potatoes instead of on a second sheet.\r\n\r\n6. Spread harissa mayo inside each pita half, then fill with sweet potatoes, avocado, a few pine nuts, and a small amount of cucumber salad. Divide stuffed pitas between plates. Add remaining cucumber salad to the side and sprinkle with remaining pine nuts.', '2019-03-27 21:20:53', 4, 2, 'other', 'able'),
(7, 'Example Article 6', 60.00, 'Example Article 6 Description', '1. Bring a large pot of salted water to a boil. Wash and dry all produce. Peel and thinly slice shallot. Thinly slice garlic. Zest lemon until you have ½ tsp; quarter lemon. Roughly chop olives. Thinly slice chili.\r\n\r\n2. Once water is boiling, add spaghetti to pot. Cook, stirring occasionally, until al dente, 9-11 minutes. Reserve ¼ cup pasta cooking water, then drain.\r\n\r\n3. Meanwhile, in a medium bowl, whisk together juice from 2 lemon wedges, a drizzle of olive oil, and lemon zest until combined. Stir in 1 TBSP shallot and season with salt and pepper.\r\n\r\n4. Heat a large drizzle of olive oil in a large pan over medium heat. Add garlic, half the olives, and remaining shallot. Cook, stirring, until softened, 2-3 minutes. If desired, add a pinch of chili for spiciness; cook for 15 seconds. Add marinara and a pinch of salt and pepper. Bring to a simmer and cook for 2 minutes, stirring a couple of times. Turn off heat.\r\n\r\n5. Add spaghetti to sauce, stirring to thoroughly coat. Stir in half the Parmesan and 2 TBSP butter. If sauce seems thick, add reserved pasta cooking water, 1 TBSP at a time, until loosened. Season with salt and pepper.\r\n\r\n6. Add arugula to bowl with dressing; season with salt and pepper and toss to thoroughly coat. Divide pasta between bowls. Top with remaining olives and remaining Parmesan. If desired, sprinkle with a pinch of remaining chili. Serve with salad on the side. Serve with remaining lemon wedges for squeezing over.', '2019-03-27 21:23:23', 4, 4, 'other', 'able'),
(8, 'Example Article 7', 70.50, 'Example Article 7 Description', '1. Adjust rack to top position and preheat oven to 425 degrees. Wash and dry all produce. Halve, peel, and finely chop shallot. Trim green beans. Mince or grate garlic. Halve demi-baguette lengthwise/\r\n\r\n2. Toss green beans on a baking sheet sheet with a drizzle of oil, salt, pepper, and chili flakes (to taste). Roast for 7 minutes (we’ll add the garlic bread then).\r\n\r\n3. Place 1 TBSP butter and garlic in a small microwave-safe bowl. Microwave until softened, 10 seconds. Spread onto cut sides of demi-baguette; season with salt and pepper. Once green beans have roasted 7 minutes, toss and push to one side of baking sheet. Add garlic bread to empty side, cut sides up. Return to oven and bake until green beans are tender and bread is lightly toasted, 5-7 minutes.\r\n\r\n4. Pat steak dry with paper towels; season all over with salt and pepper. Heat a drizzle of oil in a medium pan over medium-high heat. Add steak and cook to desired doneness, 4-7 minutes per side. Turn off heat; remove from pan and set aside to rest.\r\n\r\n5. Heat a drizzle of oil in pan used to cook steak over medium heat. Add shallot and cook, stirring, until softened, 1-2 minutes. Stir in stock concentrate and ¼ cup water. Bring to a simmer and cook, scraping up any browned bits from bottom of pan, until reduced by half, 2-3 minutes. Turn off heat; stir in 1 TBSP butter until melted. Season with salt and pepper.\r\n\r\n6. Divide steak, green beans, and garlic bread between plates. Top steak with sauce. Sprinkle green beans with chili flakes (to taste).', '2019-03-27 21:25:53', 4, 0, 'other', 'disable'),
(9, 'Example Article 8', 80.00, 'Example Article 8 Description', '1. Adjust rack to top position and preheat oven to 450 degrees. Wash and dry all produce. Cut sweet potatoes into ½-inch-thick wedges. Trim and peel onions, then cut into ½-inch-thick rings, keeping them intact. Mince a few slices until you have 2 TBSP. Drain pineapple; discard any juice.\r\n\r\n2. Toss sweet potatoes on a baking sheet with a large drizzle of oil, pepper, and a large pinch of salt. Roast, flipping halfway through, until browned and tender, 20-25 minutes. Meanwhile, in a small bowl, combine mayonnaise and sriracha (to taste).\r\n\r\n3. In a large bowl, combine beef, minced onion, 2 TBSP teriyaki sauce (you’ll use the rest later), pepper, and a couple large pinches of salt. Form into four equal-sized patties, each slightly wider than a burger bun.\r\n\r\n4. Heat a drizzle of oil in a large pan over medium-high heat (use a nonstick pan if you have one). Add pineapple and cook, stirring occasionally, until caramelized, 3-5 minutes. Transfer to a cutting board and roughly chop. Wipe out pan. Heat another drizzle of oil in same pan over medium-high heat. Add onion slices and season with salt. Cook until softened and charred, 3-4 minutes per side. Transfer to a plate.\r\n\r\n5. Heat a drizzle of oil in same pan over medium-high heat. Add patties and cook until just shy of desired doneness, 3-5 minutes per side. Transfer to a plate. Wipe out pan and return to medium-high heat. Pour in remaining teriyaki sauce and simmer until thickened, about 2 minutes. Return patties to pan, turning to coat in glaze. Cook to desired doneness, about 1 minute more.\r\n\r\n6. Halve buns. (TIP: If desired, toast buns until golden, 3-4 minutes.) Fill with glazed patties, pineapple, and onion slices. Serve sweet potato wedges and sriracha mayo on the side.', '2019-03-27 21:28:42', 1, 0, 'europe', 'able'),
(10, 'Testing Image', 1.00, 'Testing Image', 'Testing Image', '2019-03-29 19:30:59', 2, 0, 'other', 'disable'),
(11, 'Testing Image', 1.00, 'Testing Image', 'Testing Image', '2019-03-29 19:32:10', 2, 0, 'other', 'able'),
(12, 'Testing Image', 1.00, 'Testing Image', 'Testing Image', '2019-03-29 19:33:32', 2, 0, 'other', 'disable'),
(13, 'Testing Image', 1.00, 'Testing Image', 'Testing Image', '2019-03-29 19:34:25', 2, 1, 'other', 'able'),
(14, 'Testing Category', 1.00, 'Testing Category', 'Testing Category', '2019-03-30 00:10:58', 1, 0, 'europe', 'able'),
(15, 'Testing Category', 1.00, 'Testing Category', 'Testing Category\r\nTesting Editing a', '2019-04-01 02:40:21', 1, 0, 'europe', 'able'),
(16, 'Testing Compose', 12.50, 'Testing Compose', 'Testing Compose\r\nYttrium is a chemical element with symbol Y and atomic number 39. It is a silvery-metallic transition metal chemically similar to the lanthanides and has often been classified as a \"rare-earth element\".[4] Yttrium is almost always found in combination with lanthanide elements in rare-earth minerals, and is never found in nature as a free element. 89Y is the only stable isotope, and the only isotope found in the Earth\'s crust.\r\n\r\nIn 1787, Carl Axel Arrhenius found a new mineral near Ytterby in Sweden and named it ytterbite, after the village. Johan Gadolin discovered yttrium\'s oxide in Arrhenius\' sample in 1789,[5] and Anders Gustaf Ekeberg named the new oxide yttria. Elemental yttrium was first isolated in 1828 by Friedrich Wöhler.[6]\r\n\r\nThe most important uses of yttrium are LEDs and phosphors, particularly the red phosphors in television set cathode ray tube (CRT) displays.[7] Yttrium is also used in the production of electrodes, electrolytes, electronic filters, lasers, superconductors, various medical applications, and tracing various materials to enhance their properties.\r\n\r\nYttrium has no known biological role. Exposure to yttrium compounds can cause lung disease in humans.[8] ', '2019-04-01 03:01:39', 1, 0, 'chinese', 'able'),
(17, 'abcd', 0.00, 'some thing', 'no comment', '2019-04-03 16:18:40', 8, 0, 'chinese', 'able'),
(18, 'My Article 1', 30.00, 'My Description', 'Content Example:\r\n\r\nA recipe is a set of instructions that describes how to prepare or make something, especially a culinary dish. \r\n\r\nIt is also used in medicine or in information technology (user acceptance). \r\n\r\nA doctor will usually begin a prescription with recipe, Latin for take, usually abbreviated to Rx or an equivalent symbol. \r\n\r\none more line\r\n\r\none more line by admin', '2019-04-05 16:17:31', 10, 0, 'other', 'able'),
(19, 'Example for testing', 255.00, 'My Description', 'Content Example:\r\n\r\nA recipe is a set of instructions that describes how to prepare or make something, especially a culinary dish. \r\n\r\nIt is also used in medicine or in \"information technology\" (user acceptance). \r\n\r\nA doctor will usually begin a prescription with recipe, Latin for take, usually abbreviated to \'Rx\' or an equivalent symbol. ', '2019-04-09 21:36:45', 11, 0, 'chinese', 'able'),
(20, 'Check the image part is work or not', 200.00, 'Check the image part is work or not', 'Check the image part is work or not\r\nCheck the image part is work or not\r\nCheck the image part is work or not\r\nCheck the image part is work or not\r\nCheck the image part is work or notCheck the image part is work or notCheck the image part is work or notCheck the image part is work or notCheck the image part is work or notCheck the image part is work or notCheck the image part is work or notCheck the image part is work or notCheck the image part is work or notCheck the image part is work or notCheck the image part is work or notCheck the image part is work or not', '2019-04-09 22:05:12', 1, 0, 'other', 'able');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `inCartID` int(11) NOT NULL,
  `article` int(11) NOT NULL,
  `owner` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`inCartID`, `article`, `owner`) VALUES
(1, 5, 2);

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

CREATE TABLE `client` (
  `email` varchar(30) NOT NULL,
  `nickname` varchar(10) NOT NULL,
  `password` varchar(20) NOT NULL,
  `clientID` int(11) NOT NULL,
  `state` enum('able','disable') NOT NULL DEFAULT 'able'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `client`
--

INSERT INTO `client` (`email`, `nickname`, `password`, `clientID`, `state`) VALUES
('brianyauu@gmail.com', 'Brian', '12345678', 1, 'able'),
('hello@123', 'Yau', '1234', 2, 'able'),
('ha@asd', 'Peter', '12345678', 3, 'able'),
('tony@ggmail', 'Tony', '12345678', 4, 'able'),
('calvin@acbd.com', 'calvin', '12341234', 5, 'disable'),
('new@calvin.com', 'calvinnn', 'abcdefgh', 6, 'disable'),
('tonytong1998@gmail.com', 'tonytong', 'wa980511', 7, 'able'),
('chaucheukmancalvin@gmail.com', 'calvin', '12345678', 8, 'able'),
('brianyauuu@gmail.com', 'BrianYau', 'password', 9, 'able'),
('brianyauuuu@gmail.com', 'CookingMA', '12345678', 10, 'able'),
('happy@gm.com', 'Someone', '12345678', 11, 'able');

-- --------------------------------------------------------

--
-- Table structure for table `comment`
--

CREATE TABLE `comment` (
  `commentID` int(11) NOT NULL,
  `article` int(11) NOT NULL,
  `author` int(11) NOT NULL,
  `comment` text NOT NULL,
  `date` datetime NOT NULL,
  `state` enum('able','disable') NOT NULL DEFAULT 'able'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `comment`
--

INSERT INTO `comment` (`commentID`, `article`, `author`, `comment`, `date`, `state`) VALUES
(1, 1, 1, 'Content Example:\r\nABC represent an approach to training in which you can cross reference specialized example assets with corresponding documentation. Each Content Example consists of its own level within the Content Examples project. As you move through each level, you will see a series of numbered stands, each of which having its own example asset. By looking at the documentation for that Content Example and example number, you can read about how that example was created.\r\n\r\nYou should feel free to open any examples within the Content Example levels, change or edit them, make your own versions of them, and learn from how they were assembled. You may also use any of the examples in your own levels.', '2019-04-01 01:18:17', 'able'),
(2, 1, 2, 'Content Example:\r\nCBA represent an approach to training in which you can cross reference specialized example assets with corresponding documentation. Each Content Example consists of its own level within the Content Examples project. As you move through each level, you will see a series of numbered stands, each of which having its own example asset. By looking at the documentation for that Content Example and example number, you can read about how that example was created. ', '2019-04-01 01:24:03', 'disable'),
(3, 4, 2, 'testing', '2019-04-01 03:22:01', 'able'),
(4, 4, 2, 'testing\'', '2019-04-01 03:22:09', 'able'),
(5, 4, 2, 'Yttrium is a chemical element with symbol Y and atomic number 39.', '2019-04-01 03:22:22', 'able'),
(6, 5, 2, 'Yttrium is a chemical element with symbol Y and atomic number 39. It is a silvery-metallic transition metal chemically similar to the lanthanides and has often been classified as a \"rare-earth element\".[4] Yttrium is almost always found in combination with lanthanide elements in rare-earth minerals, and is never found in nature as a free element. 89Y is the only stable isotope, and the only isotope found in the Earth\'s crust.\r\n\r\nIn 1787, Carl Axel Arrhenius found a new mineral near Ytterby in Sweden and named it ytterbite, after the village. Johan Gadolin discovered yttrium\'s oxide in Arrhenius\' sample in 1789,[5] and Anders Gustaf Ekeberg named the new oxide yttria. Elemental yttrium was first isolated in 1828 by Friedrich Wöhler.[6]\r\n\r\nThe most important uses of yttrium are LEDs and phosphors, particularly the red phosphors in television set cathode ray tube (CRT) displays.[7] Yttrium is also used in the production of electrodes, electrolytes, electronic filters, lasers, superconductors, various medical applications, and tracing various materials to enhance their properties.\r\n\r\nYttrium has no known biological role. Exposure to yttrium compounds can cause lung disease in humans.[8] ', '2019-04-01 03:28:01', 'able'),
(7, 4, 8, 'Hello I am Calvin', '2019-04-03 15:59:18', 'able'),
(8, 4, 8, 'testing \'\'\'\r\nlll\'\'\'\r\n\'\'\'', '2019-04-03 16:29:18', 'able'),
(9, 7, 10, 'Hello', '2019-04-05 16:15:38', 'able'),
(10, 7, 10, 'Hello2', '2019-04-05 16:15:45', 'disable');

-- --------------------------------------------------------

--
-- Table structure for table `news`
--

CREATE TABLE `news` (
  `newsID` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `title` varchar(99) NOT NULL,
  `content` text NOT NULL,
  `author` int(11) NOT NULL,
  `type` enum('event','system') NOT NULL,
  `state` enum('able','disable') NOT NULL DEFAULT 'able'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `news`
--

INSERT INTO `news` (`newsID`, `date`, `title`, `content`, `author`, `type`, `state`) VALUES
(1, '2019-04-01 17:59:58', 'This is the first News', 'Here is Content\r\nline 2\r\n3\r\n4\r\n5\r\n6', 1, 'event', 'able'),
(2, '2019-04-01 18:07:22', 'This is the second News!', 'Here is Content\r\nline 2\r\n3\r\n4\r\n5\r\n6\r\n7', 1, 'system', 'able'),
(3, '2019-04-01 18:55:41', 'New Event!', 'Content:\r\nnoun\r\n1. Usually contents.\r\n\r\n    something that is contained: the contents of a box.\r\n    the subjects or topics covered in a book or document.\r\n    the chapters or other formal divisions of a book or document: a table of contents. \r\n\r\n2. something that is to be expressed through some medium, as speech, writing, or any of various arts: a poetic form adequate to a poetic content. \r\n\r\n3. significance or profundity; meaning: a clever play that lacks content. \r\n\r\n4. substantive information or creative material viewed in contrast to its actual or potential manner of presentation: publishers, record companies, and other content providers; a flashy website, but without much content. ', 1, 'event', 'able'),
(4, '2019-04-01 18:57:09', 'System news', 'A system is a group of interacting or interrelated entities that form a unified whole. A system is delineated by its spatial and temporal boundaries, surrounded and influenced by its environment, described by its structure and purpose and expressed in its functioning. ', 1, 'system', 'able'),
(5, '2019-04-05 17:29:33', '5/4/2019 News', '70% OFF', 1, 'event', 'able'),
(6, '2019-04-09 21:42:22', '9/4/2019', 'Testing New\r\nWrite something here\r\n\r\none more line', 1, 'event', 'able'),
(7, '2019-04-09 21:43:12', 'One New', 'A\r\nB\r\nC\r\nDFGHJKLLLLLLLLLLLLLLLLLLLLLL', 1, 'system', 'able');

-- --------------------------------------------------------

--
-- Table structure for table `record`
--

CREATE TABLE `record` (
  `recordID` int(11) NOT NULL,
  `article` int(11) NOT NULL,
  `owner` int(11) NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `record`
--

INSERT INTO `record` (`recordID`, `article`, `owner`, `date`) VALUES
(1, 4, 1, '2019-04-01 01:39:53'),
(2, 5, 1, '2019-04-01 01:40:36'),
(3, 7, 1, '2019-04-02 00:55:39'),
(4, 13, 1, '2019-04-02 00:55:39'),
(5, 4, 2, '2019-04-02 00:56:23'),
(6, 1, 2, '2019-04-02 21:01:52'),
(7, 2, 2, '2019-04-02 21:04:35'),
(8, 3, 2, '2019-04-02 21:05:34'),
(9, 6, 2, '2019-04-02 21:06:20'),
(10, 7, 2, '2019-04-02 21:06:50'),
(11, 4, 8, '2019-04-03 16:10:02'),
(12, 1, 8, '2019-04-03 16:32:55'),
(13, 7, 10, '2019-04-05 16:16:09'),
(14, 1, 10, '2019-04-05 16:16:17'),
(15, 1, 11, '2019-04-09 21:32:58'),
(16, 6, 11, '2019-04-09 21:34:50');

-- --------------------------------------------------------

--
-- Table structure for table `revenue`
--

CREATE TABLE `revenue` (
  `date` date NOT NULL,
  `revenue` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `revenue`
--

INSERT INTO `revenue` (`date`, `revenue`) VALUES
('2019-03-31', 110),
('2019-04-01', 30),
('2019-04-02', 109),
('2019-04-03', 12),
('2019-04-05', 54),
('2019-04-09', 18);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`adminID`);

--
-- Indexes for table `article`
--
ALTER TABLE `article`
  ADD PRIMARY KEY (`articleID`),
  ADD KEY `owner` (`owner`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`inCartID`),
  ADD KEY `article` (`article`),
  ADD KEY `owner` (`owner`);

--
-- Indexes for table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`clientID`);

--
-- Indexes for table `comment`
--
ALTER TABLE `comment`
  ADD PRIMARY KEY (`commentID`),
  ADD KEY `article` (`article`),
  ADD KEY `author` (`author`);

--
-- Indexes for table `news`
--
ALTER TABLE `news`
  ADD PRIMARY KEY (`newsID`),
  ADD KEY `author` (`author`);

--
-- Indexes for table `record`
--
ALTER TABLE `record`
  ADD PRIMARY KEY (`recordID`),
  ADD KEY `article` (`article`),
  ADD KEY `owner` (`owner`);

--
-- Indexes for table `revenue`
--
ALTER TABLE `revenue`
  ADD PRIMARY KEY (`date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `adminID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `article`
--
ALTER TABLE `article`
  MODIFY `articleID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `inCartID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `client`
--
ALTER TABLE `client`
  MODIFY `clientID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT for table `comment`
--
ALTER TABLE `comment`
  MODIFY `commentID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT for table `news`
--
ALTER TABLE `news`
  MODIFY `newsID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `record`
--
ALTER TABLE `record`
  MODIFY `recordID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `article`
--
ALTER TABLE `article`
  ADD CONSTRAINT `article_ibfk_1` FOREIGN KEY (`owner`) REFERENCES `client` (`clientID`);

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`article`) REFERENCES `article` (`articleID`),
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`owner`) REFERENCES `client` (`clientID`);

--
-- Constraints for table `comment`
--
ALTER TABLE `comment`
  ADD CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`article`) REFERENCES `article` (`articleID`),
  ADD CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`author`) REFERENCES `client` (`clientID`);

--
-- Constraints for table `news`
--
ALTER TABLE `news`
  ADD CONSTRAINT `news_ibfk_1` FOREIGN KEY (`author`) REFERENCES `admin` (`adminID`);

--
-- Constraints for table `record`
--
ALTER TABLE `record`
  ADD CONSTRAINT `record_ibfk_1` FOREIGN KEY (`article`) REFERENCES `article` (`articleID`),
  ADD CONSTRAINT `record_ibfk_2` FOREIGN KEY (`owner`) REFERENCES `client` (`clientID`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
