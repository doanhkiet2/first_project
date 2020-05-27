import React, { useState, useEffect } from 'react'

import { TweetList } from './list'
import { TweetCreate } from './create'
import { Tweet } from './detail'
import { apiTweetDetail } from './lookup'


export function TweetsComponent(props) {
    const [newTweets, setNewTweets] = useState([])
    const canTweet = props.canTweet === "false" ? false : true
    const handleNewTweet = (newTweet) => {
        let temNewTweets = [...newTweets]
        temNewTweets.unshift(newTweet)
        setNewTweets(temNewTweets)
    }

    return <div className={props.className}>
        {canTweet === true && <TweetCreate didTweet={handleNewTweet} className='col-12 mb-3' />}
        <TweetList newTweets={newTweets} {...props} />
    </div>
}



export function TweetDetailComponent(props) {
    const { tweetId } = props
    const [didLookup, setDidLookup] = useState(false)
    const [tweet, setTweet] = useState(null)

    const handleBackEndLookup = (response, status) => {
        if (status === 200) {
            setTweet(response)
        } else { 
            console.log(response)
            alert("there was an error finding your tweet")
        }
    }
    useEffect(() => {
        if (didLookup === false) {
            apiTweetDetail(tweetId, handleBackEndLookup)
            setDidLookup(true)
        }
    }, [tweetId, didLookup, setDidLookup])
    return tweet === null ? null : <Tweet tweet={tweet} className={props.className}/>
}










