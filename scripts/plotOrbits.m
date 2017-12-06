%%Plot orbits and density
v = VideoWriter('NesterovDensityOrbits', 'Motion JPEG AVI');
v.FrameRate = 24;
v.Quality = 100;
open(v);
timesteps = 200;
%TheMovie(timesteps) = struct('cdata', [], 'colormap', []);
for i=1:timesteps
    s = surf(times, densitySamples, log(density + 1));
    s.EdgeColor = 'none';
    caxis([0, 4]);
    xlabel('Time'); ylabel('Position'); zlabel('Density');
    zlim([0, 6])
    hold on
    scatter3(repmat(times(1, i), 1000, 1), positions(:, i), log(posdensity(:, i) + 1), 30, 3 * positions(:, 1) + 2, 'filled');
    hold off
    frame = getframe(gcf);
    writeVideo(v, frame);
end
close(v);

v = VideoWriter('NesterovOrbits', 'Motion JPEG AVI');
v.FrameRate = 24;
v.Quality = 100;
open(v);
timesteps = 200;
%TheMovie(timesteps) = struct('cdata', [], 'colormap', []);
figure();
orbits = scatter3(positions(:, 1), repmat(times(1, 1), 1000, 1), velocities(:, 1), 30, positions(:, 1));
xlabel('Position'); ylabel('Time (s)'); zlabel('Velocity');
ylim([0, 10]); zlim([-2, 2]);
view(135, 35);
frame = getframe(gcf);
writeVideo(v, frame);
hold on
for i=2:timesteps
    orbits = scatter3(positions(:, i), repmat(times(1, i), 1000, 1), velocities(:, i), 30, positions(:, 1));
    frame = getframe(gcf);
    writeVideo(v, frame);
end
hold off
close(v);