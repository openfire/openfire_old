# This document contains some simple test models and specs as an example.
# These tests were taken from the Jasmine example, and simply converted to coffeescript.
# We will completely rewrite this file and add more files to the test directory to
# test javascript code for openfire.
#   -Ethan


# Some models to test!

Player = ->
Song = ->
Player::play = (song) ->
  @currentlyPlayingSong = song
  @isPlaying = true

Player::pause = ->
  @isPlaying = false

Player::resume = ->
  throw new Error("song is already playing")  if @isPlaying
  @isPlaying = true

Player::makeFavorite = ->
  @currentlyPlayingSong.persistFavoriteStatus true

Song::persistFavoriteStatus = (value) ->

  # something complicated
  throw new Error("not yet implemented")


# The tests!

describe "Player", ->
  player = undefined
  song = undefined
  beforeEach ->
    player = new Player()
    song = new Song()

  it "should be able to play a Song", ->
    player.play song
    expect(player.currentlyPlayingSong).toEqual song

    #demonstrates use of custom matcher
    expect(player).toBePlaying song

  describe "when song has been paused", ->
    beforeEach ->
      player.play song
      player.pause()

    it "should indicate that the song is currently paused", ->
      expect(player.isPlaying).toBeFalsy()

      # demonstrates use of 'not' with a custom matcher
      expect(player).not.toBePlaying song

    it "should be possible to resume", ->
      player.resume()
      expect(player.isPlaying).toBeTruthy()
      expect(player.currentlyPlayingSong).toEqual song

  # demonstrates use of spies to intercept and test method calls
  it "tells the current song if the user has made it a favorite", ->
    spyOn song, "persistFavoriteStatus"
    player.play song
    player.makeFavorite()
    expect(song.persistFavoriteStatus).toHaveBeenCalledWith true

  #demonstrates use of expected exceptions
  describe "#resume", ->
    it "should throw an exception if song is already playing", ->
      player.play song
      expect(->
        player.resume()
      ).toThrow "song is already playing"
