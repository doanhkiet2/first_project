import React, { useEffect, useState } from 'react'
import { apiTweetList } from './lookup'
import { Tweet } from './detail'


export function TweetList(props) {
    // troi sao update nhieu lan the
    // console.log('test',props.newTweets) 
    const [tweetsInit, setTweetsInit] = useState([])
    const [tweets, setTweets] = useState([])
    const [nextUrl, setNextUrl] = useState([null])
    const [tweetsDidSet, setTweetsDidSet] = useState(false)
    useEffect(() => {
        const final = [...props.newTweets].concat(tweetsInit)
        console.log([...props.newTweets])
        if (final.length !== tweets.length) {
            setTweets(final)
        }
    }, [props.newTweets, tweets, tweetsInit])
    useEffect(() => {
        //do my lookup
        if (tweetsDidSet === false) {
            const handleTweetListLookup = (response, status) => {
                if (status === 200) {
                    setNextUrl(response.next)
                    setTweetsInit(response.results)
                    setTweetsDidSet(true)
                } else {
                    alert("there was an error")
                }
            }
            apiTweetList(props.username, handleTweetListLookup)
        }
    }, [tweetsInit, tweetsDidSet, setTweetsDidSet, props.username])


    const handleLoadNext = (event) => {
        event.preventDefault()
        if (nextUrl !== null) {
            const handleLoadNextResponse = (response, status) => {
                if (status === 200) {
                    setNextUrl(response.next)
                    const newTweets = [...tweets].concat(response.results) //why?
                    setTweetsInit(newTweets)
                    setTweets(newTweets)
                } else {
                    alert("there was an error")
                }

            }
            apiTweetList(props.username, handleLoadNextResponse, nextUrl)
        }

    }

    const handleDidRetweet = (newTweet) => {
        const updateTweetsInit = [...tweetsInit]
        updateTweetsInit.unshift(newTweet)
        setTweetsInit(updateTweetsInit)
        const updateFinalTweets = [...tweets]
        updateFinalTweets.unshift(tweets)
        setTweets(updateFinalTweets)
    }
    return <React.Fragment>{tweets.map((item, index) => {
        return <Tweet
            tweet={item}
            didRetweet={handleDidRetweet}
            key={`${index}-{tweet.id}`}
            className='my-5 py-6 border bg-white text-dark py-4' />
    })}
        {nextUrl != null && <button className='btn btn-outline-primary' onClick={handleLoadNext} >Load Next</button>}
    </React.Fragment>
}