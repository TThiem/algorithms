%%MakeMovie
v = VideoWriter('Nesterov', 'Motion JPEG AVI');
v.FrameRate = 4;
v.Quality = 100;
open(v);
timesteps = 100;
TheMovie(timesteps) = struct('cdata', [], 'colormap', []);
for i=2:timesteps - 1
    
    subplot(2, 3, 1)
    scatter(positions(:, i), velocities(:, i), 30, positions(:, 1), 'filled');
    colormap = jet;
    xlabel('Position'); ylabel('Velocity'); title('Nesterov State Space');
    xlim([-1, 1]);
    ylim([-1, 1]);
    
    subplot(2, 3, 2)
    plot(densitySamples, density(:, i), 'blue');
    xlabel('Position'); ylabel('Density'); title('Nesterov Density');
    xlim([-1, 1]);
    
    subplot(2, 3, 3)
    scatter(d2dx2density(i - 1, :), d2dt2density(i - 1,:));
    xlabel('d^2/dx^2 density'); ylabel('d^2/dt^2 density'); title('d^2/dt^2 vs d^2/dx^2 of Density');
    
    subplot(2, 3, 4)
    plot(densitySamples(2:999), d2dx2density(i - 1, :))
    xlabel('Position'); ylabel('d^2/dx^2 density'); title('d^2/dx^2');
    xlim([-1, 1]);
    
    subplot(2, 3, 5)
    plot(densitySamples(2:999), ddtdensity(i - 1, :));
    xlabel('Position'); ylabel('d/dt density'); title('d/dt');
    xlim([-1, 1]);
    
    subplot(2, 3, 6)
    scatter(d2dx2density(i - 1, :), ddtdensity(i - 1, :))
    xlabel('d^2/dx^2 density'); ylabel('d/dt density'); title('d/dt vs d^2/dx^2 of Density');
    
    frame = getframe(gcf);
    writeVideo(v, frame);
end
close(v);