# AuthChain
A blockchain implementation for authorizing uses

# Dependencies
* Tendermint
* go-lang 1.9 >

# Development Setup

## Install GO

### Getting GO
`curl https://storage.googleapis.com/golang/go1.9.1.linux-amd64.tar.gz`
`sudo tar -xvf go1.9.1.linux-amd64.tar.gz`
`sudo mv go /usr/local`
`mkdir ~/gocode`

### Set GOPATH and path for go installations to bash_profile

`export GOPATH="$HOME/gocode"`
`export PATH="$PATH:$GOPATH/bin"`
`export PATH="$PATH:/usr/local/go/bin"`

### Check for installation correctness by running

`go version`

## Install Tendermint

`go get -u github.com/tendermint/tendermint/cmd/tendermint`
## Run
`tendermint init`
`tendermint node --proxy_app=dummy`
