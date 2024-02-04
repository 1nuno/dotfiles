docker image build -t producer ./producer/.
docker image build -t consumer ./consumer/.
docker run -dit --name producer producer
docker run -dit --name consumer consumer