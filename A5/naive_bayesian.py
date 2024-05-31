# CS 131 A5
# Written by: Perucy Mussiba
# Date: 21/04/2024
# Purpose: An implementation of a naive bayes classifier in a radar classification system
#       that determines if a track is of a bird or airplane

import numpy as np
from scipy.stats import norm


# variance_likelihood determines the variance of bird and plane tracks training data and of the testing data
# gets the likelihood values of the variances of the testing data
# arguments: bird, plane and testing tracks
# returns: the maximum likelihood for bird and plane
def variance_likelihood(bird_track, plane_track, test_track):
    # determining the variance of each track
    bird_variance = np.var(bird_track, axis=1)
    plane_variance = np.var(plane_track, axis=1)
    test_variance = np.var(test_track)

    # determining the mean and std deviation of bird and plane variances
    bird_mean, bird_std = norm.fit(bird_variance)
    plane_mean, plane_std = norm.fit(plane_variance)

    # determining the likelihoods of birds and planes for the new feature (variance)
    like_birds = norm.pdf(test_variance, bird_mean, bird_std)
    like_planes = norm.pdf(test_variance, plane_mean, plane_std)

    bird_max = np.max(like_birds)
    plane_max = np.max(like_planes)

    return bird_max, plane_max


# likelihood_function gets the likelihood values of velocities in a track, adds them to an array and computes
# the maximum likelihood
# arguments: a track of velocities and the likelihoods array
# returns: the maximum likelihood for a track
def likelihood_function(vel_track, likelihood_dt):
    likelihoods = []

    for v in vel_track:
        likelihoods.append(likelihood_dt[int(v)])

    like_arr = np.array(likelihoods)
    likelihood = np.max(like_arr)
    return likelihood


# bayes_algorithm classifies a track of tracks as either a bird or plane
# arguments: cleaned test, bird and plane tracks numpy arrays and the bird and plane likelihoods for specified
#           velocities
# returns: a classification of the tracks as a list
def bayes_algorithm(test_track, bird_track, plane_track, bird_likelihoods, plane_likelihoods):
    prior_bird = 0.5
    prior_plane = 0.5
    bird_bird = 0.9
    plane_plane = 0.9
    classification = []

    # loop through the tracks to retrieve a track
    for t, track in enumerate(test_track):
        # get the likelihood value of the track belonging to a bird or a plane (feature: velocity)
        like_vel_bird = likelihood_function(track, bird_likelihoods)
        like_vel_plane = likelihood_function(track, plane_likelihoods)

        # get the likelihood value of the track belonging to a bird or a plane (feature: variance)
        like_var_bird, like_var_plane = variance_likelihood(bird_track, plane_track, track)

        # probability values using velocity as a feature
        prob_1_bird = prior_bird * like_vel_bird
        prob_1_plane = prior_plane * like_vel_plane

        # probability values using variance as a feature
        prob_2_bird = prior_bird * like_var_bird
        prob_2_plane = prior_plane * like_var_plane

        # combining the probabilities
        prob_bird = (prob_1_bird + prob_2_bird) / 2
        prob_plane = (prob_1_plane + prob_2_plane) / 2

        # normalizing the probabilities
        total_prob = prob_plane + prob_bird
        prob_bird /= total_prob
        prob_plane /= total_prob

        # classifying the track based on the largest value of the probabilities
        if prob_bird > prob_plane:
            classification.append('b')
        else:
            classification.append('a')

        # updating the prior probabilities
        if t > 0:
            if classification[t - 1] == 'b':
                prior_bird = prob_bird * bird_bird
                prior_plane = 1 - prior_bird
            else:
                prior_plane = prob_plane * plane_plane
                prior_bird = 1 - prior_plane

    return classification


# data_cleaning removes the NaN values in a row and replaces them with the mean of the non-NaN values in that row
# argument: a numpy array of tracks from the dataset.txt and testing.txt
# returns: a cleaned numpy array of track
def data_cleaning(tracks_arr):
    for j in range(tracks_arr.shape[0]):
        mean = np.nanmean(tracks_arr[j, :])
        if np.isnan(mean):
            tracks_arr[j, :] = 0
        else:
            tracks_arr[j, :] = np.where(np.isnan(tracks_arr[j, :]), mean, tracks_arr[j, :])

    return tracks_arr


# main function of the program
if __name__ == '__main__':
    # lists for respective tracks when reading data from the file
    bird_tracks = []
    plane_tracks = []
    test_tracks = []

    # reading data from the files and appending them to individual lists
    with open('likelihood.txt', 'r') as file:
        lines = file.readlines()
        bird_likelihood = np.array([float(num) for num in lines[0].split()])
        plane_likelihood = np.array([float(num) for num in lines[1].split()])

    with open('dataset.txt', 'r') as file:
        lines = file.readlines()
        for i in range(0, 10):
            bird_line = [float(num) if num != 'NaN' else np.nan for num in lines[i].split()]
            bird_tracks.append(bird_line)

        for i in range(10, 20):
            plane_line = [float(num) if num != 'NaN' else np.nan for num in lines[i].split()]
            plane_tracks.append(plane_line)

    with open('testing.txt', 'r') as file:
        lines = file.readlines()
        for i in range(0, 10):
            test_line = [float(num) if num != 'NaN' else np.nan for num in lines[i].split()]
            test_tracks.append(test_line)

    # converting the lists to numpy arrays for easy mathematical operations
    bird_tracks_arr = np.array(bird_tracks)
    plane_tracks_arr = np.array(plane_tracks)
    test_tracks_arr = np.array(test_tracks)

    # data cleaning of NaN values
    bird_tracks_clean = data_cleaning(bird_tracks_arr)
    plane_tracks_clean = data_cleaning(plane_tracks_arr)
    test_tracks_clean = data_cleaning(test_tracks_arr)

    # getting the classification of the test tracks as a list
    result = bayes_algorithm(test_tracks_clean, bird_tracks_clean, plane_tracks_clean, bird_likelihood,
                             plane_likelihood)

    # processing the returned track classifications into a readable format
    output = []
    for i in range(0, 10):
        output.append((f"O{i + 1}: {result[i]}"))

    # printing the final classification
    print(output)
