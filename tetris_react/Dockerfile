# Pull official base image
FROM node:latest

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
COPY package-lock.json ./

# install react-scripts
RUN npm install .
RUN npm install react-scripts

# add app
COPY . ./

CMD ["npm", "start"]