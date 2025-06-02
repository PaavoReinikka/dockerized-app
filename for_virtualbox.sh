
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# install deno
curl -fsSL https://deno.land/install.sh | sh

deno upgrade

# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome*.deb
sudo apt install xclip

# for git
ssh-keygen -t ed25519 -C "paavo.reinikka@proton.me"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub | xclip
# Now save the pub key to github keys

git clone git@github.com:wumpfroot/Eprice.git

cd Eprice/App/client
deno install --allow-sctips

sudo apt install tmux

# RUN E2E-TESTS: docker compose run --rm --entrypoint=npx e2e-tests playwright test
# RUN endpoint tests: docker compose --profile backend-tests up (assuming the test container has been built)

