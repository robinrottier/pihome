
$image="pihome"

function build()
{
    if (test-path "Dockerfile")
    {
        $df = "Dockerfile"
        $ct = ".."
    }
    elseif (test-path "docker\Dockerfile")
    {
        $df = "docker\Dockerfile"
        $ct = "."
    }
    else
    {
        throw "Cant find dockerfile? Run either from project directory or project/docker folder"
    }
    
    docker build -t $image -f $df $ct
}

function killRunning()
{
    docker kill $image 2>&1 | out-null
}

function run()
{
    killRunning

    docker run --rm --name $image -p 7080:80 -p 7081:3306 -d $image
}

function shell()
{
    docker exec -it $image ash
}

function runAll()
{
    "Run docker build..."
    build
    if ($LASTEXITCODE -ne 0) { write-host -ForegroundColor Red "...failed ($LASTEXITCODE)"; return }

    return

    "Running detached image..."
    run
    if ($LASTEXITCODE -ne 0) { write-host -ForegroundColor Red "...failed ($LASTEXITCODE)"; return }

    "Starting shell..."
    shell
    if ($LASTEXITCODE -ne 0) { write-host -ForegroundColor Red "...failed ($LASTEXITCODE)"; return }
}

if ($args[0])
{
    &$args[0]
}
else
{
    runAll    
}
