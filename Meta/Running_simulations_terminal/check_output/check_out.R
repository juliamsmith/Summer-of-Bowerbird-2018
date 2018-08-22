# remember to set current directory to here
library(tidyverse)

to_check <- "D_strat=0.15_pmar=0.05_dim=2250_repair_4"
my_dir <- paste0("../to_store/", to_check, "/results/")

# load the first result file available
my_file <- list.files(my_dir)[1]

df <- read_csv(paste0(my_dir, my_file))

# check that times make sense
# these should be around 360hrs
df %>% ggplot(aes(x = repairing_hrs + staying_hrs + foraging_hrs + marauding_hrs + traveling_hrs)) + geom_histogram()

# time per event
df %>% ggplot(aes(x = repairing_hrs / repairing_events)) + 
  geom_histogram(binwidth = 0.01) + ggtitle("Time for repairing event")

df %>% ggplot(aes(x = foraging_hrs / foraging_events)) + 
  geom_histogram(binwidth = 0.01) + ggtitle("Time for foraging event")

df %>% ggplot(aes(x = staying_hrs / staying_events)) + 
  geom_histogram(binwidth = 0.01) + ggtitle("Time for staying event")

df %>% ggplot(aes(x = traveling_hrs / traveling_events)) + 
  geom_histogram(binwidth = 0.002) + ggtitle("Time for travel event")

df %>% ggplot(aes(x = marauding_hrs / marauding_events)) + 
  geom_histogram(binwidth = 0.02) + ggtitle("Time for maraud event")

## number of reproductive events
print(sum(df$successful_mating))

## number marauding events
print(sum(df$marauding_events))

print(sum(df$repairing_hrs) / sum(df$marauding_events))

df %>% ggplot(aes(x = repairing_hrs / 4)) + geom_histogram(binwidth = 1)
