import React, { useState } from 'react'
import { ActionBtn } from './button'
import {
    UserDisplay,
    UserPicture
}
    from '../profiles'


function ParentTweet(props) {
    const { tweet } = props
    // console.log(tweet.parent, 'aaa')
    return (tweet.parent ? <Tweet isReTweet reTweeter={props.reTweeter} hideActions className={' '} tweet={tweet.parent} /> : null
    )
}



export function Tweet(props) {
    const { tweet, didRetweet, hideActions, isReTweet, reTweeter } = props
    const [actionTweet, setActionTweet] = useState(props.tweet ? props.tweet : null)

    const path = window.location.pathname
    const idRegex = /(?<tweetid>\d+)/
    const match = path.match(idRegex)
    const urlTweetId = match ? match.groups.tweetid : -1
    const isDetail = `${tweet.id}` === `${urlTweetId}`

    const handleLink = (event) => {
        event.preventDefault()
        window.location.href = `tweets/${tweet.id}`
    }


    const handlePerformAction = (newActionTweet, status) => {
        if (status === 200) {
            setActionTweet(newActionTweet)
        } else if (status === 201) {
            if (didRetweet) {
                didRetweet(newActionTweet)
                // console.log(newActionTweet)
            }
        }
    }

    let className = props.className ? props.className : 'col-10 max-auto col-md-6 py-4'
    className = isReTweet === true ? `${className} border rounded` : className
    return <div className={className}>
        {isReTweet === true && <div className='mb-2'>
            <span className='small text-muted p-2'>Retweet via <UserDisplay user={reTweeter} /></span>
        </div>}
        <div className="d-flex">
            <div className="col-1">
                <UserPicture user={tweet.user} />
            </div>
            <div className="col-11">
                <div>
                    <p>
                        <UserDisplay includeFullName user={tweet.user} />
                    </p>
                    <p>{tweet.content}</p>
                    <ParentTweet tweet={tweet} reTweeter={tweet.user} />
                </div>
                <div className='btn btn-group px-0'>
                    {(actionTweet && hideActions !== true) && <React.Fragment>
                        <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{ type: "like", display: "Likes" }} />
                        <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{ type: "unlike", display: "Unlike" }} />
                        <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{ type: "retweet", display: "Retweet" }} />
                    </React.Fragment>
                    }
                    {isDetail === true ? null : <button className='btn btn-outline-primary' onClick={handleLink}>View</button>}
                </div>
            </div>
        </div>
    </div>

}   
